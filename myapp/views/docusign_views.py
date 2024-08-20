# docusign_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib
import base64
import json

# Use the provided secret key for HMAC verification
SECRET_KEY = '02nDEQKCN6pJmFRsTo3QHSuU0AKA8P/gILd1dZ+rzZQ='

@csrf_exempt
def docusign_webhook(request):
    if request.method == 'POST':
        # HMAC verification (if enabled in DocuSign)
        if 'X-DocuSign-Signature-1' in request.headers:
            signature = request.headers.get('X-DocuSign-Signature-1')
            data = request.body
            calculated_signature = base64.b64encode(hmac.new(SECRET_KEY.encode(), data, hashlib.sha256).digest()).decode()
            
            if not hmac.compare_digest(signature, calculated_signature):
                return JsonResponse({'status': 'signature mismatch'}, status=400)
        
        # Process the incoming JSON payload
        envelope_data = json.loads(request.body.decode('utf-8'))
        
        # Check the event type and handle accordingly
        envelope_status = envelope_data.get('status')
        if envelope_status == 'sent':
            print("Envelope sent:", envelope_data)
            # Add your logic here (e.g., update your database, notify the sender)
        elif envelope_status == 'delivered':
            print("Envelope delivered:", envelope_data)
            # Add your logic here
        elif envelope_status == 'signed':
            print("Envelope signed:", envelope_data)
            # Add your logic here
        elif envelope_status == 'completed':
            print("Envelope completed:", envelope_data)
            # Add your logic here
        
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
