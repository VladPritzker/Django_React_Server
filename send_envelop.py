import sys
import os
import django

# Setup the environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Setup Django before importing models
django.setup()

# Now import your Django models
from myapp.models import DocuSignToken
from decouple import config
import requests

def send_envelop(template_choice=None):
    if not template_choice:
        # Default value if no template is passed
        template_choice = input("Enter template choice (1 for Template 1, 2 for Template 2): ")

    # Retrieve token from the database
    token_entry = DocuSignToken.objects.first()
    if not token_entry:
        print("No DocuSign token found in the database.")
        return
    
    access_token = token_entry.access_token
    
    # Determine template ID
    if template_choice == "1":
        template_id = "17cc51e1-5433-4576-98bb-7c60bde50bbd"
    elif template_choice == "2":
        template_id = "fc1fa3af-f87d-4558-aa10-6b275852c78e"
    else:
        print("Invalid template selection.")
        return
    
    # Send the envelope
    account_id = config('DOCUSIGN_ACCOUNT_ID')
    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    
    payload = {
        "templateId": template_id,
        "status": "sent"  # Send the envelope immediately
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        print("Envelope sent successfully!")
    else:
        print(f"Error sending envelope: {response.json()}")

# Call the function to send the envelope
send_envelop()
