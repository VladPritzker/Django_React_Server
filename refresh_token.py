import django
from django.conf import settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
import base64
import requests
from myapp.models import DocuSignToken
import logging
import schedule
import time

# Set up Django environment

# Configure logging
logging.basicConfig(level=logging.INFO)  # Change this to DEBUG if you need more detailed logs

def refresh_docusign_token():
    # Retrieve the latest tokens from the database
    logging.info("Attempting to retrieve the token entry from the database")
    
    token_entry = DocuSignToken.objects.first()

    if not token_entry:
        logging.error("No DocuSign token entry found in the database.")
        return

    logging.info(f"Old Access Token: {token_entry.access_token}")
    logging.info(f"Old Refresh Token: {token_entry.refresh_token}")

    url = "https://account-d.docusign.com/oauth/token"

    # Generate the Basic Authorization code
    logging.info("Generating the Basic Authorization code")
    
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

    logging.info("Sending POST request to refresh token")

    try:
        response = requests.post(url, headers=headers, data=data)
        logging.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            tokens = response.json()
            logging.info("Tokens refreshed successfully")
            
            # Update the tokens in the database
            token_entry.access_token = tokens.get('access_token')
            token_entry.refresh_token = tokens.get('refresh_token')
            token_entry.save()

            logging.info(f"New Access Token: {tokens.get('access_token')}")
            logging.info(f"New Refresh Token: {tokens.get('refresh_token')}")
        else:
            logging.error(f"Failed to refresh token: {response.status_code} - {response.text}")
            if 'invalid_grant' in response.text:
                logging.error("The refresh token is invalid or expired.")
            raise Exception(f"Failed to refresh token: {response.text}")
    
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise e

# Ensure the function is called
if __name__ == "__main__":
    logging.info("Starting the token refresh process")
    refresh_docusign_token()


def start_scheduler():
    schedule.every(6).hours.do(refresh_docusign_token)

    logging.info("Starting the token refresh scheduler...")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
 