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

def refresh_access_token():
    # Implement the OAuth 2.0 Token Refresh flow here
    # You might need client_id, client_secret, and refresh_token from settings
    # This is a simplified example
    import requests

    token_url = 'https://account.docusign.com/oauth/token'
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': settings.DOCUSIGN_REFRESH_TOKEN,
        'client_id': settings.DOCUSIGN_CLIENT_ID,
        'client_secret': settings.DOCUSIGN_CLIENT_SECRET,
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        new_access_token = response.json().get('access_token')
        # Update the TOKEN variable and settings
        global TOKEN
        TOKEN = new_access_token
        settings.DOCUSIGN_ACCESS_TOKEN = new_access_token
        return new_access_token
    else:
        print(f"Failed to refresh access token: {response.json()}")
        return None


TOKEN = settings.DOCUSIGN_ACCESS_TOKEN
account_id = settings.DOCUSIGN_ACCOUNT_ID
template_id = settings.DOCUSIGN_TEMPLATE_ID



def send_envelop(recipient_email, recipient_name):
    """Send an envelope using a predefined template ID and recipient details."""
    
    access_token = TOKEN
    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    
    payload = {
        "templateId": template_id,
        "status": "sent",  # Send the envelope immediately
        "templateRoles": [
            {
                "email": recipient_email,
                "name": recipient_name,
                "roleName": "Signer"  # Adjust the role name if necessary
            }
        ]
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        # Envelope sent successfully
        envelope_id = response.json().get('envelopeId')
        return {'envelope_id': envelope_id}
    elif response.status_code == 401:
        # Unauthorized, try to refresh the token
        print(f"Unauthorized: {response.json()} - Token might have expired")
        new_token = refresh_access_token()
        if new_token:
            headers["Authorization"] = f"Bearer {new_token}"
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 201:
                envelope_id = response.json().get('envelopeId')
                return {'envelope_id': envelope_id}
            else:
                error_message = response.json()
                print(f"Error sending envelope after token refresh: {error_message}")
                raise Exception(f"Error sending envelope after token refresh: {error_message}")
        else:
            print("Could not refresh token")
            raise Exception("Could not refresh token")
    else:
        # Handle other errors
        error_message = response.json()
        print(f"Error sending envelope: {error_message}")
        raise Exception(f"Error sending envelope: {error_message}")

