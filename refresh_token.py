import base64
import requests
from django.conf import settings
from myapp.models import DocuSignToken  # Assuming the model is in the same app

def refresh_docusign_token():
    # Retrieve the latest tokens from the database
    token_entry = DocuSignToken.objects.first()

    if not token_entry:
        raise Exception("No DocuSign token entry found in the database.")

    url = "https://account-d.docusign.com/oauth/token"
    
    # Generate the Basic Authorization code
    auth_str = f"{settings.DOCUSIGN_CLIENT_ID}:{settings.DOCUSIGN_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()  # Base64 encode the client_id:client_secret
    
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': token_entry.refresh_token,
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        # Update the tokens in the database
        token_entry.access_token = tokens['access_token']
        token_entry.refresh_token = tokens['refresh_token']
        token_entry.save()
        
        return tokens['access_token']
    else:
        raise Exception(f"Failed to refresh token: {response.text}")

if __name__ == "__main__":
    refresh_docusign_token()
