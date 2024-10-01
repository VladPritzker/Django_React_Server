import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.views.docusign_views.send_envelop import send_envelop  # Assuming your send_envelop is in docsign_integration.py

@csrf_exempt
def send_docusign_envelope(request):
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            recipient_email = data.get('email')
            recipient_name = data.get('name')

            if not recipient_email or not recipient_name:
                return JsonResponse({'error': 'Missing recipient email or name'}, status=400)

            # Call the function to send the envelope
            send_envelop(recipient_email, recipient_name)
            
            return JsonResponse({'message': 'Envelope sent successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
