import os
import json
import requests
import logging
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from myapp.models import DocuSignToken, DocuSignSignature
import boto3
from botocore.exceptions import NoCredentialsError


logger = logging.getLogger(__name__)

DO_SPACES_KEY = 'DO004MHYF2464638EKXE'
DO_SPACES_SECRET = '7MzQUzaWWwPHQGmzmyRBQBg6wb31DKurv6sM2UFBbmI'
DO_SPACES_REGION = 'nyc3'
DO_SPACES_BUCKET = 'docusign55'
DO_SPACES_ENDPOINT = f'https://{DO_SPACES_BUCKET}.{DO_SPACES_REGION}.digitaloceanspaces.com'

# DocuSign API Configuration
DS_API_BASE_PATH = 'https://demo.docusign.net/restapi/v2.1'

def get_access_token():
    """Retrieve the latest access token from the database."""
    token_entry = DocuSignToken.objects.first()
    if not token_entry:
        raise Exception("No DocuSign token entry found in the database.")
    return token_entry.access_token

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            # Retrieve and log the raw POST data
            raw_data = request.body.decode('utf-8')
            logger.debug(f"Received raw POST request: {raw_data}")

            # Parse the JSON data
            envelope_data = json.loads(raw_data)
            logger.debug(f"Parsed JSON data: {json.dumps(envelope_data, indent=2)}")

            # Extract the envelopeId
            envelope_id = envelope_data.get('data', {}).get('envelopeId', None)
            if envelope_id:
                logger.debug(f"Extracted Envelope ID: {envelope_id}")
                print(f"Extracted Envelope ID: {envelope_id}")  # Console log

                # Fetch the form data JSON
                form_data = fetch_envelope_form_data(envelope_id)

                if form_data:
                    # Extract form data fields
                    form_data_items = {item['name']: item['value'] for item in form_data.get('formData', [])}
                    signer_email = form_data_items.get('email_of_signer')
                    signer_name = form_data_items.get('name_of_signer')
                    date_of_birth = form_data_items.get('date_of_birth')
                    date_signed = form_data_items.get('date_signed')

                    # Extract additional recipient data
                    recipient_data = form_data.get('recipientFormData', [])[0] if form_data.get('recipientFormData') else None
                    if recipient_data:
                        recipient_id = recipient_data.get('recipientId')

                        # Convert date formats if necessary
                        date_of_birth = datetime.strptime(date_of_birth, '%m.%d.%Y').date()  # assuming format is mm.dd.yyyy
                        date_signed = datetime.strptime(date_signed, '%m/%d/%Y').date()  # assuming format is mm/dd/yyyy

                        # Store the extracted data in the database
                        DocuSignSignature.objects.create(
                            envelope_id=envelope_id,
                            recipient_id=recipient_id,
                            email_of_signer=signer_email,
                            name_of_signer=signer_name,
                            date_of_birth=date_of_birth,
                            date_signed=date_signed
                        )

                # Download the PDF document and save it to both server and local machine
                download_and_save_pdf(envelope_id)

                return JsonResponse({'status': 'success', 'message': f'PDF and form data retrieved and stored for Envelope ID {envelope_id}'}, status=200)
            else:
                logger.error("Envelope ID not found in the request data.")
                return JsonResponse({'status': 'error', 'message': 'Envelope ID not found'}, status=400)
        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            print(f"Error processing the webhook: {str(e)}")  # Console log for errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




def fetch_envelope_form_data(envelope_id):
    """Fetch the form data JSON for the given envelope ID."""
    try:
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/form_data'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            form_data = response.json()
            print(f"Retrieved form data for Envelope ID {envelope_id}: {json.dumps(form_data, indent=2)}")
            return form_data
        else:
            logger.error(f"Failed to fetch form data, status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Exception occurred while fetching form data: {str(e)}")


s3_client = boto3.client(
    's3',
    endpoint_url=DO_SPACES_ENDPOINT,
    aws_access_key_id=DO_SPACES_KEY,
    aws_secret_access_key=DO_SPACES_SECRET
)

def download_and_save_pdf(envelope_id):
    """Download the combined PDF document for the given envelope ID and upload it to DigitalOcean Spaces."""
    try:
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Create an in-memory file-like object for the PDF
            pdf_data = response.content
            file_name = f"envelope_{envelope_id}_combined.pdf"
            bucket_folder = 'Docusign_PDF/'

            try:
                # Upload the PDF to DigitalOcean Spaces
                s3_client.put_object(
                    Bucket=DO_SPACES_BUCKET,
                    Key=bucket_folder + file_name,
                    Body=pdf_data,
                    ContentType='application/pdf'
                )
                print(f"Uploaded PDF to DigitalOcean Spaces: {DO_SPACES_ENDPOINT}/{bucket_folder}{file_name}")
            except NoCredentialsError as e:
                logger.error(f"Credentials not available for DigitalOcean Spaces: {str(e)}")
            except Exception as e:
                logger.error(f"Failed to upload PDF to DigitalOcean Spaces: {str(e)}")

        else:
            logger.error(f"Failed to download PDF, status code: {response.status_code}")

    except Exception as e:
        logger.error(f"Exception occurred during PDF download: {str(e)}")