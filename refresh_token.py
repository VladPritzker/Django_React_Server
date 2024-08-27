import os
import requests
from django.conf import settings

def refresh_docusign_token():
    url = "https://account-d.docusign.com/oauth/token"
    headers = {
        'Authorization': f'Basic {settings.DOCUSIGN_CLIENT_ID}:{settings.DOCUSIGN_CLIENT_SECRET}',
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
        # Optionally update your .env file or database with the new tokens
        with open('.env', 'w') as f:
            f.write(f"DOCUSIGN_CLIENT_ID={settings.DOCUSIGN_CLIENT_ID}\n")
            f.write(f"DOCUSIGN_CLIENT_SECRET={settings.DOCUSIGN_CLIENT_SECRET}\n")
            f.write(f"DOCUSIGN_REFRESH_TOKEN={settings.DOCUSIGN_REFRESH_TOKEN}\n")
            f.write(f"DOCUSIGN_ACCESS_TOKEN={settings.DOCUSIGN_ACCESS_TOKEN}\n")
        return tokens['access_token']
    else:
        raise Exception("Failed to refresh token")

if __name__ == "__main__":
    refresh_docusign_token()
