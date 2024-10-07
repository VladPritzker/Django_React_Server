import requests
import os
from django.conf import settings  # Correct import for Django settings


ENVELOPE_LOG_FILE = "downloaded_envelopes.txt"
# File to store the downloaded envelope IDs
# TOKEN_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../myapp/views/docusign_views/token.txt'))
# ACCOUNT_ID = "docusign_config.txt"

def load_config(file_path):
    """Load DocuSign account_id configuration file."""
    config = {}
    if not os.path.exists(file_path):
        raise Exception(f"Configuration file not found: {file_path}")

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split('=')
            config[key] = value
    return config

def get_downloaded_envelopes():
    if os.path.exists(ENVELOPE_LOG_FILE):
        with open(ENVELOPE_LOG_FILE, 'r') as file:
            downloaded_envelopes = file.read().splitlines()
    else:
        downloaded_envelopes = []
    return set(downloaded_envelopes)

def save_downloaded_envelope(envelope_id):
    with open(ENVELOPE_LOG_FILE, 'a') as file:
        file.write(f"{envelope_id}\n")

TOKEN = settings.DOCUSIGN_ACCESS_TOKEN
ACCOUNT_ID = settings.DOCUSIGN_ACCOUNT_ID
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

def get_signed_envelopes():
    access_token = TOKEN
    account_id = ACCOUNT_ID



    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    url = f"https://demo.docusign.net/restapi/v2.1/accounts/{account_id}/envelopes"
    params = {
        "from_date": "2023-09-10T00:00:00Z",
        "status": "completed"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        envelopes = response.json().get('envelopes', [])
        return envelopes
    else:
        print(f"Error fetching envelopes: {response.status_code}")
        return []

# def download_pdf(envelope_id):
#     access_token = TOKEN
#     url = f'https://demo.docusign.net/restapi/v2.1/accounts/28621645/envelopes/{envelope_id}/documents/combined'
#     headers = {
#         'Authorization': f'Bearer {access_token}'
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         # Save the PDF with the envelope ID as the filename
#         file_path = f'/Users/vladbuzhor/downloads/hosted_completed_envelopes/{envelope_id}.pdf'
#         with open(file_path, 'wb') as file:
#             file.write(response.content)
#         print(f"PDF for envelope {envelope_id} downloaded successfully!")
#         return True
#     else:
#         print(f"Failed to download PDF for envelope {envelope_id}: {response.status_code}")
#         return False

# def process_envelopes():
#     downloaded_envelopes = get_downloaded_envelopes()
#     signed_envelopes = get_signed_envelopes()

#     for envelope in signed_envelopes:
#         envelope_id = envelope['envelopeId']
#         if envelope_id not in downloaded_envelopes:
#             print(f"Downloading PDF for new envelope: {envelope_id}")
#             if download_pdf(envelope_id):
#                 save_downloaded_envelope(envelope_id)
#         else:
#             print(f"Envelope {envelope_id} already downloaded. Skipping...")
# # Execute the envelope processing function
# process_envelopes()
