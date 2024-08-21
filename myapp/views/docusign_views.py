import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import os

logger = logging.getLogger(__name__)

# DocuSign API Configuration
DS_API_BASE_PATH = 'https://demo.docusign.net/restapi/v2.1'
ACCESS_TOKEN = 'your_access_token_here'  # Replace with your actual token
ACCOUNT_ID = '29035884'

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

                # Download the combined PDF document
                download_pdf(envelope_id)

                return JsonResponse({'status': 'success', 'envelopeId': envelope_id}, status=200)
            else:
                logger.error("Envelope ID not found in the request data.")
                return JsonResponse({'status': 'error', 'message': 'Envelope ID not found'}, status=400)

        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            print(f"Error processing the webhook: {str(e)}")  # Console log for errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def download_pdf(envelope_id):
    """Download the combined PDF document for the given envelope ID."""
    try:
        url = f'{DS_API_BASE_PATH}/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Save the PDF to the filesystem
            file_path = os.path.join('downloads', f"envelope_{envelope_id}_combined.pdf")

            # Ensure the 'downloads' directory exists
            if not os.path.exists('downloads'):
                os.makedirs('downloads')

            with open(file_path, 'wb') as f:
                f.write(response.content)
                logger.debug(f"Downloaded combined document to {file_path}")
                print(f"Downloaded combined document to {file_path}")  # Console log
        else:
            logger.error(f"Failed to download document: {response.text}")
            print(f"Failed to download document: {response.text}")  # Console log

    except Exception as e:
        logger.error(f"Error downloading the document: {str(e)}")
        print(f"Error downloading the document: {str(e)}")  # Console log
