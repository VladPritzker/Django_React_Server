import json
import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import os

logger = logging.getLogger(__name__)

# DocuSign API Configuration
DS_API_BASE_PATH = 'https://demo.docusign.net/restapi/v2.1'
ACCESS_TOKEN = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwCANs27wsLcSAgAgHbwyQXD3EgCAJHARGQRmJtIuQ5UZS71Mq0VAAEAAAAYAAEAAAAFAAAADQAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkIgAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkMACAp4qIwsLcSDcAjwPrez9MtESeuaWmpmPIgA.zcZSO2rOyKsxMvOg9bnGzgJgeCgX2Ol03_ZGP8HX2iwezxLUhRQTw6NIN2hSDbeHR8RFzWREP3hWYskZ31rtTy55udMuO-SrDI8sH_UEo2coL1B70Q11Oh2ZfKEnpsqLJ7tP6PNTL7D-NdaiZiRl7VIp4jgEnCjEoInxIOfpnPuEeF8QhO08vUvOL6CnwV2fVtFoA9ynFQ_vMm7oM6sYoFfJ_ODIbN2veX5pqhDFYJF4qFG3wNr4Yee0alnwFVpxnpfo-cYlt1ocqa0b9t2bB-aVmTqN8tTX8YUjAfowYKB4sc_farw6SonNxF4HKPxnC6ktzcIWV270VvCbJCn6gQ'  # Replace with your actual token
ACCOUNT_ID = '29035884'

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            # Retrieve and log the raw POST data
            raw_data = request.body.decode('utf-8')
            logger.debug(f"Received raw POST request: {raw_data}")
            logger.debug(f"Parsed JSON data: {json.dumps(envelope_data, indent=2)}")


            # Parse the JSON data
            envelope_data = json.loads(raw_data)
            logger.debug(f"Parsed JSON data: {json.dumps(envelope_data, indent=2)}")

            # Extract the envelopeId
            envelope_id = envelope_data.get('data', {}).get('envelopeId', None)
            if envelope_id:
                logger.debug(f"Extracted Envelope ID: {envelope_id}")
                print(f"Extracted Envelope ID: {envelope_id}")  # Console log

                # Download the combined PDF document
                response = download_pdf(envelope_id)

                if response:
                    return response  # Return the PDF as an HTTP response
                else:
                    return JsonResponse({'status': 'error', 'message': 'Failed to download PDF'}, status=500)

            else:
                logger.error("Envelope ID not found in the request data.")
                return JsonResponse({'status': 'error', 'message': 'Envelope ID not found'}, status=400)

        except Exception as e:
            logger.error(f"Error processing the webhook: {str(e)}")
            print(f"Error processing the webhook: {str(e)}")  # Console log for errors
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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


def download_pdf(envelope_id):
    """Download the combined PDF document for the given envelope ID."""
    try:
        url = f'{DS_API_BASE_PATH}/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
        headers = {
            'Authorization': f'Bearer {ACCESS_TOKEN}'
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Serve the PDF as a file download
            file_name = f"envelope_{envelope_id}_combined.pdf"
            http_response = HttpResponse(response.content, content_type='application/pdf')
            http_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return http_response

        else:
            return None
    except Exception as e:
        return None 