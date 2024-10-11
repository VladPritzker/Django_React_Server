# plaid_client.py
from django.conf import settings
from plaid import ApiClient
from plaid.api import plaid_api
from plaid.models import (
    ItemPublicTokenExchangeRequest,
    LinkTokenCreateRequest,
    LinkTokenCreateRequestUser,
    Products,
    CountryCode
)
from plaid.configuration import Configuration

configuration = Configuration(
    host='https://sandbox.plaid.com',  # Use the appropriate URL for your environment
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET,
    }
)
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)
