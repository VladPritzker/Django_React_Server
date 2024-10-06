import os
import requests
from django.conf import settings  # Correct import for Django settings

# File paths for tokens (assuming token.txt is in the root of your project)
# TOKEN_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../myapp/views/docusign_views/token.txt'))

# def load_access_token():
#     """Load the access token from the token.txt file."""
#     if not os.path.exists(TOKEN_FILE):
#         raise Exception(f"Token file not found: {TOKEN_FILE}")

#     with open(TOKEN_FILE, 'r') as file:
#         lines = file.readlines()
#         for line in lines:
#             if line.startswith("token="):
#                 return line.split('=')[1].strip()
#     raise Exception("Access token not found in the token file")

# Token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwCATV8vSuLcSAgAgI2CPY3i3EgCALlaeBAx3T9DhTXhXpK7bj8VAAEAAAAYAAEAAAAFAAAADQAkAAAAOTYzOGE4MzItM2Q4ZC00YzczLWI4YzQtMDMyM2ZmM2FhMWE3IgAkAAAAOTYzOGE4MzItM2Q4ZC00YzczLWI4YzQtMDMyM2ZmM2FhMWE3EgACAAAACwAAAGludGVyYWN0aXZlBwAAAHNlY19rZXkwAAA2qwJK4txI.BExQ4a4nk6LTRj2BWZEJe-BHLep40TrKXrSWpr3_q6__0uqlIV2n58T4KAl-hQM8giOPiRhw1MT7WokKJrokHbwmt8ukFHS_Q-1Gm_p4o0rv9yX2uGJQfZ_WQCPn9xukoKrQPXO7fyvHLQpcIp7W93GmAFYm7-v-QYEMaIAU-7YToUcMidW2LPmxKiHeU1r5INsrzvVlqyskwDkf44rptZcTZr3TDH107cJ2yEELYLdJda9uPvFcxpEQaDZJR56z6ctuorfOoNk8wg-W0r61z2YXuKHi126CoanEE588Gxl3LqsUGboUPUG-833BSYXkh1F8p3gtTUlPRzt2oArgEw'

TOKEN = settings.DOCUSIGN_ACCESS_TOKEN
account_id = settings.DOCUSIGN_ACCOUNT_ID
template_id = settings.DOCUSIGN_TEMPLATE_ID



def send_envelop(recipient_email, recipient_name):
    """Send an envelope using a predefined template ID and recipient details."""
    
    # Load the access token from settings or file
    access_token = TOKEN

    # Retrieve account ID and template ID from settings
    
    # Prepare the payload with recipient info
    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    
    payload = {
        "templateId": template_id,
        "status": "sent",  # Send the envelope immediately
        "templateRoles": [
            {
                "email": recipient_email,
                "name": recipient_name,
                "roleName": "Signer"  # Assuming the role of the recipient is "Signer"
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Send the envelope
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Envelope sent successfully!")
    elif response.status_code == 401:
        print(f"Unauthorized: {response.json()} - Token might have expired")
        # Refresh token and retry
        new_token = refresh_access_token()
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print("Envelope sent successfully after token refresh!")
            else:
                print(f"Error sending envelope after refresh: {response.json()}")
        else:
            print("Could not refresh token")
    else:
        print(f"Error sending envelope: {response.json()}")
