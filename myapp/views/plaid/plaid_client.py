# plaid_client file
from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from django.conf import settings
import certifi
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Determine the Plaid environment based on settings
plaid_env = getattr(settings, 'PLAID_ENV', 'sandbox')  # Defaults to 'sandbox' if PLAID_ENV is not set

# Choose the appropriate host and credentials based on environment
if plaid_env == 'production':
    plaid_host = "https://production.plaid.com"
    plaid_secret = settings.PLAID_SECRET  # Production secret from settings
else: 
    plaid_host = "https://sandbox.plaid.com"
    plaid_secret = settings.PLAID_SANDBOX_SECRET  # Use the secret from settings

# Log the environment and credentials for debugging
logger.info(f"Using Plaid Environment: {plaid_env}")
logger.info(f"Using Plaid Client ID: {settings.PLAID_CLIENT_ID}")
logger.info(f"Using Plaid Secret: {plaid_secret}")


# Get the path to certifi's certificates
certifi_cert_path = certifi.where()

# Set up Plaid configuration
configuration = Configuration(
    host=plaid_host,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': plaid_secret,
    },
    ssl_ca_cert=certifi_cert_path  
)

# Create the API client and Plaid client
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)
