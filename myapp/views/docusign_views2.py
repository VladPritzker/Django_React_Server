import os
import json
import requests
import logging
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from myapp.models import DocuSignToken, DocuSignSignature, DocuSignSignatureTemplate2
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


s3_client = boto3.client(
    's3',
    endpoint_url=DO_SPACES_ENDPOINT,
    aws_access_key_id=DO_SPACES_KEY,
    aws_secret_access_key=DO_SPACES_SECRET
)

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

            # Extract the envelopeId and templateId
            envelope_id = envelope_data.get('data', {}).get('envelopeId', None)
            template_id = envelope_data.get('data', {}).get('templateId', None)

            logger.debug(f"Extracted Envelope ID: {envelope_id}, Template ID: {template_id}")
            print(f"Extracted Envelope ID: {envelope_id}, Template ID: {template_id}")  # Console log

            if envelope_id:
                # Fetch the form data JSON
                form_data = fetch_envelope_form_data(envelope_id)

                if form_data:
                    # Store the form data and PDF based on the template_id
                    if template_id == "17cc51e1-5433-4576-98bb-7c60bde50bbd":
                        # Store for Template 1 (Different Folder and Table)
                        store_template1_data(form_data, envelope_id)
                        download_and_save_pdf(envelope_id, "Template1")
                    elif template_id == "fc1fa3af-f87d-4558-aa10-6b275852c78e":
                        # Store for Template 2 (Different Folder and Table)
                        store_template2_data(form_data, envelope_id)
                        download_and_save_pdf(envelope_id, "Template2")
                    else:
                        logger.error("Unknown template ID.")
                        return JsonResponse({'status': 'error', 'message': 'Unknown template ID'}, status=400)

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

def store_template1_data(form_data, envelope_id):
    """Store form data for Template 1 in the corresponding table and folder."""
    json_data = json.dumps(form_data, indent=2).encode('utf-8')
    file_name = f"envelope_{envelope_id}_formdata.json"
    
    # Folder for Template 1
    bucket_folder = 'Docusign_JSON/Template1/'

    try:
        # Upload the JSON to DigitalOcean Spaces for Template 1
        s3_client.put_object(
            Bucket=DO_SPACES_BUCKET,
            Key=bucket_folder + file_name,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"Uploaded JSON to DigitalOcean Spaces: {DO_SPACES_ENDPOINT}/{bucket_folder}{file_name}")

        # Save to Template 1 specific table in the database
        recipient_data = form_data.get('recipientFormData', [])[0]
        DocuSignSignature.objects.create(
            envelope_id=envelope_id,
            recipient_id=recipient_data.get('recipientId'),
            email_of_signer=recipient_data.get('email'),
            name_of_signer=recipient_data.get('name'),
            date_of_birth=recipient_data.get('date_of_birth')
        )
        logger.info(f"Stored data for Envelope ID {envelope_id} in Template 1 table")

    except NoCredentialsError as e:
        logger.error(f"Credentials not available for DigitalOcean Spaces: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to store Template 1 data: {str(e)}")

def store_template2_data(form_data, envelope_id):
    """Store form data for Template 2 in the corresponding table and folder."""
    json_data = json.dumps(form_data, indent=2).encode('utf-8')
    file_name = f"envelope_{envelope_id}_formdata.json"
    
    # Folder for Template 2
    bucket_folder = 'Docusign_JSON/Template2/'

    try:
        # Upload the JSON to DigitalOcean Spaces for Template 2
        s3_client.put_object(
            Bucket=DO_SPACES_BUCKET,
            Key=bucket_folder + file_name,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"Uploaded JSON to DigitalOcean Spaces: {DO_SPACES_ENDPOINT}/{bucket_folder}{file_name}")

        # Save to Template 2 specific table in the database
        recipient_data = form_data.get('recipientFormData', [])[0]
        DocuSignSignatureTemplate2.objects.create(
            envelope_id=envelope_id,
            recipient_id=recipient_data.get('recipientId'),
            email_of_signer=recipient_data.get('email'),
            name_of_signer=recipient_data.get('name'),
            date_of_birth=recipient_data.get('date_of_birth')
        )
        logger.info(f"Stored data for Envelope ID {envelope_id} in Template 2 table")

    except NoCredentialsError as e:
        logger.error(f"Credentials not available for DigitalOcean Spaces: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to store Template 2 data: {str(e)}")

def download_and_save_pdf(envelope_id, template_folder):
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
            
            # Folder for each template
            bucket_folder = f'Docusign_PDF/{template_folder}/'

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
