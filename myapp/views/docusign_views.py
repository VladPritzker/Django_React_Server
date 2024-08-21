import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

# Configure logging
logger = logging.getLogger(__name__)

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            # Retrieve and log the raw POST data
            raw_data = request.body.decode('utf-8')
            logger.debug(f"Received POST request from DocuSign: {raw_data}")

            # Parse the JSON data
            envelope_data = json.loads(raw_data)
            logger.debug(f"Parsed JSON data: {json.dumps(envelope_data, indent=2)}")

            # Extract the envelopeId from the nested data
            envelope_id = envelope_data.get('data', {}).get('envelopeId', 'No Envelope ID found')
            logger.debug(f"Extracted Envelope ID: {envelope_id}")

            # Respond with success status
            return JsonResponse({'status': 'success', 'envelopeId': envelope_id}, status=200)
        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
