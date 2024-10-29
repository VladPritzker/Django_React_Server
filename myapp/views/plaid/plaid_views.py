#  plaid_views file
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .plaid_client import plaid_client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.country_code import CountryCode  # Ensure this import is present
from django.conf import settings  # Import settings for accessing environment variables
from plaid.model.products import Products
from myapp.models import PlaidItem  # Import the PlaidItem model



import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def create_link_token(request):
    try:
        user_id = "34"  # Replace with actual user ID as needed
        logger.info(f"Creating link token for client_user_id: {user_id}")

        # Remove client_id and secret from the request data
        request_data = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name="Pritzker Finance",
            products=[Products("transactions")],
            country_codes=[CountryCode("US")],
            language="en",
            webhook="https://oyster-app-vhznt.ondigitalocean.app/plaid/webhook/"
        )

        # Send the request to Plaid
        response = plaid_client.link_token_create(request_data)
        link_token = response.link_token

        # Log and return the link token
        logger.info(f"Link token generated: {link_token}")
        return JsonResponse({'link_token': link_token})

    except Exception as e:
        logger.error(f"Error creating link token: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_access_token(request):
    try:
        data = json.loads(request.body)
        public_token = data.get('public_token')
        user_id = data.get('user_id')
        logger.info(f"Received public token: {public_token} for user_id: {user_id}")

        # Exchange public token for access token
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)

        # Extract access token and item ID
        access_token = exchange_response.access_token
        item_id = exchange_response.item_id
        logger.info(f"Access token: {access_token}, Item ID: {item_id}")

        # Update the PlaidItem for the user
        plaid_item, created = PlaidItem.objects.get_or_create(user_id=user_id)
        if plaid_item.item_id != item_id:
            plaid_item.previous_item_id = plaid_item.item_id
            plaid_item.item_id = item_id
            plaid_item.cursor = None  # Reset the cursor when item_id changes
        plaid_item.access_token = access_token
        plaid_item.save()

        return JsonResponse({'message': 'Access token obtained successfully.', 'access_token': access_token})
    except Exception as e:
        logger.error(f"Error getting access token: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_account_data(request):
    try:
        data = json.loads(request.body)
        access_token = data.get('access_token')
        if not access_token:
            return JsonResponse({'error': 'Access token missing'}, status=400)
        
        # Use the utility function
        accounts = get_account_data_util(access_token)
        if accounts is None:
            return JsonResponse({'error': 'Failed to get account data'}, status=500)
        
        # Convert accounts to dictionary format
        accounts_data = [account.to_dict() for account in accounts]
        return JsonResponse({'accounts': accounts_data})
    except Exception as e:
        logger.error(f"Error getting account data: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

        
@csrf_exempt
def get_account_data_util(access_token):
    try:
        # Fetch account data from Plaid using the access token
        request_data = AccountsGetRequest(access_token=access_token)
        response = plaid_client.accounts_get(request_data)
        # Return the account data
        return response.accounts
    except Exception as e:
        logger.error(f"Error getting account data: {str(e)}")
        return None
