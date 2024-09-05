import os
import django
import requests
from decouple import config

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from myapp.models import DocuSignToken

# Load environment variables
account_id = config('DOCUSIGN_ACCOUNT_ID')
template_id = "17cc51e1-5433-4576-98bb-7c60bde50bbd"  # You can also put this in .env if needed
url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"

# Retrieve the latest access token from the database
token_entry = DocuSignToken.objects.first()
if not token_entry:
    raise Exception("No DocuSign token entry found in the database.")
access_token = token_entry.access_token

# Print the retrieved access token to verify
print(f"Access Token retrieved from DB: {access_token}")

# Prompt for the number of recipients
num_recipients = int(input("Enter the number of recipients: "))

# Initialize the list to hold template roles
template_roles = []

# Collect information for each recipient
for i in range(num_recipients):
    print(f"Enter details for recipient {i+1}:")
    email = input("Enter email: ")
    name = input("Enter name: ")
    role_name = input("Enter role name (e.g., Recipient): ")
    
    # Create a template role dictionary and append to the list
    template_roles.append({
        "email": email,
        "name": name,
        "roleName": role_name,
        "clientUserId": "6444c091-9811-489b-b90e-54652ef532ad"  # This can be dynamic or static
    })

# Construct the payload
payload = {
    "templateId": template_id,
    "templateRoles": template_roles,
    "status": "sent"
}

# Set up the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Send the envelope
response = requests.post(url, headers=headers, json=payload)

# Check the response
if response.status_code == 201:
    print("Envelope sent successfully!")
else:
    print(f"Failed to send envelope. Status code: {response.status_code}")
    print(f"Response: {response.json()}")
