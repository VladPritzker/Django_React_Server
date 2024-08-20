import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

# DocuSign API Configuration
DS_API_BASE_PATH = 'https://demo.docusign.net/restapi/v2.1'
ACCESS_TOKEN = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQsAAAABAAUABwCACTWJG8HcSAgAgElYl17B3EgCAJHARGQRmJtIuQ5UZS71Mq0VAAEAAAAYAAEAAAAFAAAADQAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkIgAkAAAAN2E2ZDg3NTgtMWU2Zi00NmJiLWFkMGEtNTVmOTBlOTEwNGVkEgABAAAACwAAAGludGVyYWN0aXZlMACAD61gG8HcSDcAjwPrez9MtESeuaWmpmPIgA.n7o-85sRW0W99CeqeC8YeK_B9s-N1eJQvuTAp3troFBjS1iH5Q4YHDjdhNgxABzfz-WkD_iqKaIP09u-U0qAR409tFs1xPdLfmlgAon7Xh1mI9Jc2yYgLjGdLY_UgG22lv7X--WjIjjZouRT-gy4rGR8Kv2blhOa2AVMi2mEif9YEBu2N2HB8oriiyLHsvzWQNx7FCGm2ij-coIHaNPuvotPCCR7iVLOznsjEYxoT-ZNmGeboTtjLa080Owav--DI6A9LgH8fmEBhz6gIRFWzBcv5RtB_s4ASgF0H6sj8FqJbbQKpnhxLpL_g5M93juw_-qo59RdPqVzFjaxt_H3oQ'  # Replace with your actual token
ACCOUNT_ID = '29035884'

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        try:
            envelope_data = json.loads(request.body.decode('utf-8'))
            envelope_id = envelope_data.get('envelopeId')

            # Call the DocuSign API to download the combined document
            url = f'{DS_API_BASE_PATH}/accounts/{ACCOUNT_ID}/envelopes/{envelope_id}/documents/combined'
            headers = {
                'Authorization': f'Bearer {ACCESS_TOKEN}'
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                # Save the combined document to the filesystem
                file_path = os.path.join('downloads', f"envelope_{envelope_id}_combined.pdf")

                # Ensure the 'downloads' directory exists
                if not os.path.exists('downloads'):
                    os.makedirs('downloads')

                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f"Downloaded combined document to {file_path}")

                return JsonResponse({'status': 'success', 'message': f'Documents for envelope {envelope_id} downloaded successfully.'}, status=200)
            else:
                print(f"Failed to download document: {response.text}")
                return JsonResponse({'status': 'error', 'message': 'Failed to download document.'}, status=500)

        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'status': 'error', 'message': f'Unexpected error: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
