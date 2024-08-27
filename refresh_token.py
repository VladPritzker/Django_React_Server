import base64
import os
import requests
from django.conf import settings

def refresh_docusign_token():
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
        'refresh_token': settings.DOCUSIGN_REFRESH_TOKEN,
    }
    
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        tokens = response.json()
        # Save the new access_token and refresh_token
        settings.DOCUSIGN_ACCESS_TOKEN = tokens['access_token']
        settings.DOCUSIGN_REFRESH_TOKEN = tokens['refresh_token']
        
        # Write the Basic Authorization code to the .env file
        with open('.env', 'w') as f:
            f.write(f"DOCUSIGN_CLIENT_ID={settings.DOCUSIGN_CLIENT_ID}\n")
            f.write(f"DOCUSIGN_CLIENT_SECRET={settings.DOCUSIGN_CLIENT_SECRET}\n")
            f.write(f"DOCUSIGN_REFRESH_TOKEN={settings.DOCUSIGN_REFRESH_TOKEN}\n")
            f.write(f"DOCUSIGN_ACCESS_TOKEN={settings.DOCUSIGN_ACCESS_TOKEN}\n")
            f.write(f"DOCUSIGN_AUTHORIZATION_CODE=Basic {b64_auth_str}\n")
        
        return tokens['access_token']
    else:
        raise Exception(f"Failed to refresh token: {response.text}")

if __name__ == "__main__":
    refresh_docusign_token()
