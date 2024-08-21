import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            raw_data = request.body.decode('utf-8')
            logger.debug(f"Received raw POST request: {raw_data}")

            envelope_data = json.loads(raw_data)
            logger.debug(f"Parsed JSON data: {json.dumps(envelope_data, indent=2)}")

            # Extract the envelopeId and log it to the console
            envelope_id = envelope_data.get('data', {}).get('envelopeId', 'No Envelope ID found')
            logger.debug(f"Extracted Envelope ID: {envelope_id}")
            print(f"Extracted Envelope ID: {envelope_id}")  # Console log

            return JsonResponse({'status': 'success', 'envelopeId': envelope_id}, status=200)
        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            print(f"Error processing the webhook: {str(e)}")  # Console log for errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
