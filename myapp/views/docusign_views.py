import os
import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.conf import settings
from myapp.models import DocuSignToken

logger = logging.getLogger(__name__)

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

                # Download the PDF document and save it to both server and local machine
                download_and_save_pdf(envelope_id)

                return JsonResponse({'status': 'success', 'message': f'PDF downloaded for Envelope ID {envelope_id}'}, status=200)
            else:
                logger.error("Envelope ID not found in the request data.")
                return JsonResponse({'status': 'error', 'message': 'Envelope ID not found'}, status=400)
        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            print(f"Error processing the webhook: {str(e)}")  # Console log for errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def download_and_save_pdf(envelope_id):
    """Download the combined PDF document for the given envelope ID and save it."""
    try:
        access_token = get_access_token()
        url = f'{DS_API_BASE_PATH}/accounts/{settings.DOCUSIGN_ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Save the PDF to a file on the server
            server_folder_path = "./envelopes"
            os.makedirs(server_folder_path, exist_ok=True)
            server_file_name = os.path.join(server_folder_path, f"envelope_{envelope_id}_combined.pdf")
            with open(server_file_name, 'wb') as pdf_file:
                pdf_file.write(response.content)

            print(f"Downloaded PDF: {server_file_name}")
        else:
            logger.error(f"Failed to download PDF, status code: {response.status_code}")

    except Exception as e:
        logger.error(f"Exception occurred during PDF download: {str(e)}")

if __name__ == "__main__":
    envelope_id = input("Enter the Envelope ID: ")
    download_and_save_pdf(envelope_id)

@csrf_exempt
def download_envelope_pdf(request):
    if request.method == 'GET':
        envelope_id = request.GET.get('envelope_id')
        if envelope_id:
            response = download_pdf(envelope_id)
            if response:
                return response
            else:
                return HttpResponse('Failed to download PDF', status=500)
        else:
            return HttpResponse('Envelope ID is required', status=400)

    return HttpResponse('Invalid request method', status=405)
