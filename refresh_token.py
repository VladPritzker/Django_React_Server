import os
import django
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
import base64
import requests
from django.conf import settings
from myapp.models import DocuSignToken
import logging
import schedule
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

def refresh_docusign_token():
    # Retrieve the latest tokens from the database
    token_entry = DocuSignToken.objects.first()

    if not token_entry:
        logging.error("No DocuSign token entry found in the database.")
        return

    logging.info(f"Old Access Token: {token_entry.access_token}")
    logging.info(f"Old Refresh Token: {token_entry.refresh_token}")

    url = "https://account-d.docusign.com/oauth/token"
    
    # Generate the Basic Authorization code
    auth_str = f"{settings.DOCUSIGN_CLIENT_ID}:{settings.DOCUSIGN_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    
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

        logging.info(f"New Access Token: {tokens['access_token']}")
        logging.info(f"New Refresh Token: {tokens['refresh_token']}")
        logging.info("Token refreshed successfully")
        return tokens['access_token']
    else:
        logging.error(f"Failed to refresh token: {response.text}")
        if 'invalid_grant' in response.text:
            logging.error("The refresh token is invalid or expired. Manual intervention required.")
        raise Exception(f"Failed to refresh token: {response.text}")

ef start_scheduler():
    schedule.every(5).hours.do(refresh_docusign_token)

    logging.info("Starting the token refresh scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
