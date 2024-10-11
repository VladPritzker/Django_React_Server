from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .plaid_client import plaid_client
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest  # For fetching account data
from django.conf import settings
import json

# Mock storage for access tokens (use a database in production)
user_access_tokens = {}

@require_http_methods(["GET"])
def create_link_token(request):
    try:
        # Generate a unique user ID (use the logged-in user's ID in a real application)
        user_id = str(request.user.id) if request.user.is_authenticated else 'anonymous_user'

        request_data = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id=user_id),
            client_name='Your App Name',
            products=[Products('transactions')],
            country_codes=[CountryCode('US')],
            language='en',
        )
        response = plaid_client.link_token_create(request_data)
        link_token = response.link_token
        return JsonResponse({'link_token': link_token})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Handle CSRF tokens properly in production
@require_http_methods(["POST"])
def get_access_token(request):
    try:
        data = json.loads(request.body)
        public_token = data.get('public_token')

        # Create the exchange request
        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = plaid_client.item_public_token_exchange(exchange_request)
        access_token = exchange_response.access_token
        item_id = exchange_response.item_id

        # Store access_token and item_id securely in your database associated with the user
        user_access_tokens[request.user.id] = access_token  # Mock storing token for demo purposes

        print(f'Access Token: {access_token}')
        print(f'Item ID: {item_id}')

        return JsonResponse({'message': 'Access token obtained successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_account_data(request):
    try:
        user_id = request.user.id
        access_token = user_access_tokens.get(user_id)  # Retrieve access token from mock storage
        
        if not access_token:
            return JsonResponse({'error': 'No access token found for this user.'}, status=400)

        # Create the request to fetch account data
        request_data = AccountsGetRequest(access_token=access_token)
        response = plaid_client.accounts_get(request_data)

        # Return the account data
        return JsonResponse(response.to_dict())
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
