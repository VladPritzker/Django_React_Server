# plaid_client.py
from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from django.conf import settings
import certifi
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Log the PLAID_CLIENT_ID and PLAID_SECRET for debugging
logger.info(f"Using Plaid Client ID: {settings.PLAID_CLIENT_ID}")
logger.info(f"Using Plaid Secret: {settings.PLAID_SECRET}")

# Get the path to certifi's certificates
certifi_cert_path = certifi.where()

# Set up Plaid configuration
configuration = Configuration(
    host="https://production.plaid.com",
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    },
    ssl_ca_cert=certifi_cert_path  
)

# Create the API client and Plaid client
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)
