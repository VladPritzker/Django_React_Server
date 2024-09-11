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
            raw_data = request.body.decode('utf-8')
            envelope_data = json.loads(raw_data)

            envelope_id = envelope_data.get('data', {}).get('envelopeId', None)
            template_id = envelope_data.get('data', {}).get('templateId', None)

            if envelope_id:
                # If template ID is missing, fetch it using the additional API request
                if not template_id:
                    template_id = fetch_template_id(envelope_id)

                if template_id:
                    # Fetch form data from DocuSign
                    form_data = fetch_envelope_form_data(envelope_id)

                    if form_data:
                        # Store the PDF and recipient data based on template_id
                        if template_id == "17cc51e1-5433-4576-98bb-7c60bde50bbd":
                            store_template1_data(envelope_id)  # Store PDF
                            save_recipient_data(form_data, envelope_id, 'template1')  # Save recipient data
                        elif template_id == "fc1fa3af-f87d-4558-aa10-6b275852c78e":
                            store_template2_data(envelope_id)  # Store PDF
                            save_recipient_data(form_data, envelope_id, 'template2')  # Save recipient data
                        else:
                            return JsonResponse({'status': 'error', 'message': 'Unknown template ID'}, status=400)

                    return JsonResponse({'status': 'success', 'message': 'PDF and form data saved.'}, status=200)
                else:
                    logger.error(f"Could not retrieve template ID for Envelope ID {envelope_id}")
                    return JsonResponse({'status': 'error', 'message': 'Template ID not found'}, status=400)
            else:
                return JsonResponse({'status': 'error', 'message': 'Envelope ID not found'}, status=400)
        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




def store_template1_data(envelope_id):
    """Download and store the combined PDF for Template 1 in DigitalOcean Spaces."""
    file_name = f"envelope_{envelope_id}_combined.pdf"
    
    # Folder for Template 1
    bucket_folder = 'Docusign_PDF/Template1/'

    try:
        # Download the combined PDF
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Store the PDF in DigitalOcean Spaces
            pdf_data = response.content
            s3_client.put_object(
                Bucket=DO_SPACES_BUCKET,
                Key=bucket_folder + file_name,
                Body=pdf_data,
                ContentType='application/pdf'
            )
            print(f"Uploaded PDF to DigitalOcean Spaces: {DO_SPACES_ENDPOINT}/{bucket_folder}{file_name}")

            logger.info(f"Stored PDF for Envelope ID {envelope_id} in Template 1 folder")

        else:
            logger.error(f"Failed to download PDF for Envelope ID {envelope_id}, status code: {response.status_code}")

    except NoCredentialsError as e:
        logger.error(f"Credentials not available for DigitalOcean Spaces: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to store PDF for Template 1: {str(e)}")

def store_template2_data(envelope_id):
    """Download and store the combined PDF for Template 2 in DigitalOcean Spaces."""
    file_name = f"envelope_{envelope_id}_combined.pdf"
    
    # Folder for Template 2
    bucket_folder = 'Docusign_PDF/Template2/'

    try:
        # Download the combined PDF
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Store the PDF in DigitalOcean Spaces
            pdf_data = response.content
            s3_client.put_object(
                Bucket=DO_SPACES_BUCKET,
                Key=bucket_folder + file_name,
                Body=pdf_data,
                ContentType='application/pdf'
            )
            print(f"Uploaded PDF to DigitalOcean Spaces: {DO_SPACES_ENDPOINT}/{bucket_folder}{file_name}")

            logger.info(f"Stored PDF for Envelope ID {envelope_id} in Template 2 folder")

        else:
            logger.error(f"Failed to download PDF for Envelope ID {envelope_id}, status code: {response.status_code}")

    except NoCredentialsError as e:
        logger.error(f"Credentials not available for DigitalOcean Spaces: {str(e)}")
    except Exception as e:
        logger.error(f"Failed to store PDF for Template 2: {str(e)}")



def save_recipient_data(form_data, envelope_id, template_type):
    """Save recipient data to the correct database table based on the template type."""
    try:
        recipient_form_data = form_data.get('recipientFormData', [])[0]  # Assuming only one recipient
        
        if recipient_form_data:
            # Extract the form data fields
            form_fields = {item['name']: item['value'] for item in recipient_form_data.get('formData', [])}
            
            recipient_id = recipient_form_data.get('recipientId')
            email_of_signer = form_fields.get('email_of_signer')
            name_of_signer = form_fields.get('name_of_signer')
            date_of_birth_str = form_fields.get('date_of_birth')
            date_signed_str = form_fields.get('date_signed')

            # Convert date_of_birth and date_signed to proper date formats
            date_of_birth = datetime.strptime(date_of_birth_str, "%m.%d.%Y").date() if date_of_birth_str else None
            date_signed = datetime.strptime(date_signed_str, "%m/%d/%Y").replace(tzinfo=None) if date_signed_str else None

            # Save to the appropriate table based on the template type
            if template_type == 'template1':
                DocuSignSignature.objects.create(
                    envelope_id=envelope_id,
                    recipient_id=recipient_id,
                    email_of_signer=email_of_signer,
                    name_of_signer=name_of_signer,
                    date_of_birth=date_of_birth,
                    date_signed=date_signed
                )
                logger.info(f"Stored data for Envelope ID {envelope_id} in Template 1 table")
            else:
                DocuSignSignatureTemplate2.objects.create(
                    envelope_id=envelope_id,
                    recipient_id=recipient_id,
                    email_of_signer=email_of_signer,
                    name_of_signer=name_of_signer,
                    date_of_birth=date_of_birth,
                    date_signed=date_signed
                )
                logger.info(f"Stored data for Envelope ID {envelope_id} in Template 2 table")
        else:
            logger.error(f"No recipient data found for Envelope ID {envelope_id}")

    except Exception as e:
        logger.error(f"Failed to store recipient data for Envelope ID {envelope_id}: {str(e)}")


def fetch_envelope_form_data(envelope_id):
    """Fetch form data for a given envelope using the DocuSign API."""
    try:
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/form_data'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            form_data = response.json()
            logger.info(f"Form data retrieved for Envelope ID {envelope_id}: {json.dumps(form_data, indent=2)}")
            return form_data
        else:
            logger.error(f"Failed to fetch form data for Envelope ID {envelope_id}, status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"Exception occurred while fetching form data for Envelope ID {envelope_id}: {str(e)}")
        return None


def fetch_template_id(envelope_id):
    """Fetch the template ID using the DocuSign API for a given envelope ID."""
    try:
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/templates'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            template_data = response.json()
            # Check if any templates exist and extract the first template's ID
            if template_data.get('templates'):
                template_id = template_data['templates'][0].get('templateId')
                logger.info(f"Retrieved template ID: {template_id} for Envelope ID: {envelope_id}")
                return template_id
            else:
                logger.error(f"No templates found for Envelope ID: {envelope_id}")
                return None
        else:
            logger.error(f"Failed to fetch template ID, status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching template ID for Envelope ID {envelope_id}: {str(e)}")
        return None
