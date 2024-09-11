# views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from myapp.models import DocuSignToken
from decouple import config
import requests

def send_envelop(request):
    if request.method == 'POST':
        template_choice = request.POST.get('template_choice')
        num_recipients = int(request.POST.get('num_recipients'))
        
        # Retrieve token from the database
        token_entry = DocuSignToken.objects.first()
        if not token_entry:
            return JsonResponse({"error": "No DocuSign token found in the database."}, status=400)
        
        access_token = token_entry.access_token
        
        # Determine template ID
        if template_choice == "1":
            template_id = "17cc51e1-5433-4576-98bb-7c60bde50bbd"
        elif template_choice == "2":
            template_id = "fc1fa3af-f87d-4558-aa10-6b275852c78e"
        else:
            return JsonResponse({"error": "Invalid template selection."}, status=400)
        
        # Construct template roles from form input
        template_roles = []
        for i in range(1, num_recipients + 1):
            email = request.POST.get(f'email_{i}')
            name = request.POST.get(f'name_{i}')
            role_name = request.POST.get(f'role_name_{i}')
            
            template_roles.append({
                "email": email,
                "name": name,
                "roleName": role_name,
                "clientUserId": "6444c091-9811-489b-b90e-54652ef532ad"
            })
        
        # Send the envelope
        account_id = config('DOCUSIGN_ACCOUNT_ID')
        url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
        
        payload = {
            "templateId": template_id,
            "templateRoles": template_roles,
            "status": "sent"
        }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            return JsonResponse({"success": "Envelope sent successfully!"}, status=201)
        else:
            return JsonResponse({"error": response.json()}, status=response.status_code)
    
    return render(request, 'send_envelope.html')
