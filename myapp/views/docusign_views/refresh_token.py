import os
import base64
import urllib.request
import urllib.parse
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)

# File paths
TOKEN_FILE = 'token.txt'
REFRESH_TOKEN_FILE = 'refresh_token.txt'
DOCUSIGN_CONFIG_FILE = 'docusign_config.txt'  # Path to the file containing client ID and secret

# DocuSign token URL
DOCUSIGN_REFRESH_TOKEN_URL = 'https://account-d.docusign.com/oauth/token'


def load_config(file_path):
    """Load DocuSign client ID and secret from the configuration file."""
    config = {}
    if not os.path.exists(file_path):
        raise Exception(f"Configuration file not found: {file_path}")

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key] = value
    return config


def save_to_file(file_path, token, last_updated):
    """Save the token and last updated time to a file."""
    with open(file_path, 'w') as f:
        f.write(f"token={token}\n")
        f.write(f"last_updated={last_updated}\n")


def load_from_file(file_path):
    """Load the token and last updated time from a file."""
    if not os.path.exists(file_path):
        return None, None

    with open(file_path, 'r') as f:
        lines = f.readlines()
        token = lines[0].strip().split('=')[1]
        last_updated = lines[1].strip().split('=')[1]
    return token, last_updated


def refresh_docusign_token():
    """Refresh the DocuSign token and update the token and refresh token files."""
    logging.info("Attempting to retrieve the DocuSign credentials from the config file")

    # Load the client ID and client secret from the config file
    config = load_config(DOCUSIGN_CONFIG_FILE)
    DOCUSIGN_CLIENT_ID = config.get('DOCUSIGN_CLIENT_ID')
    DOCUSIGN_CLIENT_SECRET = config.get('DOCUSIGN_CLIENT_SECRET')

    # Load the refresh token from file
    refresh_token, last_updated_refresh = load_from_file(REFRESH_TOKEN_FILE)

    if not refresh_token:
        logging.error("No refresh token found.")
        return

    logging.info(f"Old Refresh Token: {refresh_token}")

    # Generate the Basic Authorization code
    logging.info("Generating the Basic Authorization code")
    auth_str = f"{DOCUSIGN_CLIENT_ID}:{DOCUSIGN_CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }).encode()

    # Send the POST request using urllib
    logging.info("Sending POST request to refresh token")

    try:
        req = urllib.request.Request(DOCUSIGN_REFRESH_TOKEN_URL, data=data, headers=headers)
        with urllib.request.urlopen(req) as response:
            response_data = response.read().decode()
            logging.info(f"Response status: {response.status}")

            if response.status == 200:
                tokens = json.loads(response_data)
                logging.info("Tokens refreshed successfully")
                new_access_token = tokens.get('access_token')
                new_refresh_token = tokens.get('refresh_token')

                # Save the new tokens to their respective files
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_to_file(TOKEN_FILE, new_access_token, now)
                save_to_file(REFRESH_TOKEN_FILE, new_refresh_token, now)

                logging.info(f"New Access Token saved: {new_access_token}")
                logging.info(f"New Refresh Token saved: {new_refresh_token}")
            else:
                logging.error(f"Failed to refresh token: {response.status}")
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        raise e


if __name__ == "__main__":
    logging.info("Starting the token refresh process")
    refresh_docusign_token()
