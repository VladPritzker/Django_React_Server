# docusign_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
from docusign_esign import ApiClient, EnvelopesApi

# DocuSign API Configuration
DS_API_BASE_PATH = 'https://demo.docusign.net/restapi'  # Use demo for testing; switch to production URL in live environment
ACCESS_TOKEN = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQsAAAABAAUABwCACTWJG8HcSAgAgElYl17B3EgCAJHARGQRmJtIuQ5UZS71Mq0VAAEAAAAYAAEAAAAFAAAADQAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkIgAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkEgABAAAACwAAAGludGVyYWN0aXZlMACAD61gG8HcSDcAjwPrez9MtESeuaWmpmPIgA.n7o-85sRW0W99CeqeC8YeK_B9s-N1eJQvuTAp3troFBjS1iH5Q4YHDjdhNgxABzfz-WkD_iqKaIP09u-U0qAR409tFs1xPdLfmlgAon7Xh1mI9Jc2yYgLjGdLY_UgG22lv7X--WjIjjZouRT-gy4rGR8Kv2blhOa2AVMi2mEif9YEBu2N2HB8oriiyLHsvzWQNx7FCGm2ij-coIHaNPuvotPCCR7iVLOznsjEYxoT-ZNmGeboTtjLa080Owav--DI6A9LgH8fmEBhz6gIRFWzBcv5RtB_s4ASgF0H6sj8FqJbbQKpnhxLpL_g5M93juw_-qo59RdPqVzFjaxt_H3oQ'  # Replace with your OAuth access token
ACCOUNT_ID = '29035884'  # Replace with your DocuSign account ID

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            # Process the incoming JSON payload
            envelope_data = json.loads(request.body.decode('utf-8'))
            
            # Check the event type and handle accordingly
            envelope_status = envelope_data.get('status')
            envelope_id = envelope_data.get('envelopeId')

            if envelope_status == 'sent':
                # If the envelope is sent, download the documents
                download_envelope_documents(envelope_id)
                return JsonResponse({'status': 'success', 'message': f"Documents for envelope {envelope_id} downloaded successfully."}, status=200)
            else:
                return JsonResponse({'status': 'ignored', 'message': f"Envelope status {envelope_status} not handled."}, status=200)

        except (KeyError, ) as e:
            print(f"Error processing webhook: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def download_envelope_documents(envelope_id):
    """Download the documents of an envelope."""
    api_client = ApiClient()
    api_client.host = DS_API_BASE_PATH
    api_client.set_default_header("Authorization", f"Bearer {ACCESS_TOKEN}")

    envelopes_api = EnvelopesApi(api_client)

    # Fetch the envelope documents
    documents_list = envelopes_api.list_documents(ACCOUNT_ID, envelope_id)

    for document in documents_list.envelope_documents:
        document_id = document.document_id

        # Download each document
        document_content = envelopes_api.get_document(ACCOUNT_ID, envelope_id, document_id)
        file_path = os.path.join('downloads', f"envelope_{envelope_id}_document_{document_id}.pdf")

        # Ensure the 'downloads' directory exists
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        with open(file_path, 'wb') as f:
            f.write(document_content)
            print(f"Downloaded document {document_id} to {file_path}")
