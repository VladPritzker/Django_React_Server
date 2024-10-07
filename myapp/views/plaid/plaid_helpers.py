import json
import uuid

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from plaid.api import plaid_api
from plaid import ApiClient, Configuration
from plaid.rest import ApiException

# Import models from their specific modules
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

from myapp.models import PlaidItem  # Import your PlaidItem model




def get_plaid_client():
    configuration = Configuration(
        host=settings.PLAID_HOST,
        api_key={
            'clientId': settings.PLAID_CLIENT_ID,
            'secret': settings.PLAID_SECRET,
        }
    )
    api_client = ApiClient(configuration)
    client = plaid_api.PlaidApi(api_client)
    return client




def create_link_token(request):
    client = get_plaid_client()
    try:
        if request.user.is_authenticated:
            client_user_id = str(request.user.id)
        else:
            # Generate a unique client_user_id for unauthenticated users
            client_user_id = str(uuid.uuid4())

        request_data = LinkTokenCreateRequest(
            client_name="Your App",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=client_user_id
            ),
            products=[Products('transactions')],
        )
        response = client.link_token_create(request_data)
        return JsonResponse({'link_token': response.link_token})
    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt  # If you cannot include CSRF tokens from the frontend
def exchange_public_token(request):
    client = get_plaid_client()

    try:
        body_data = json.loads(request.body)
        public_token = body_data.get('public_token')

        if not public_token:
            return JsonResponse({'error': 'public_token is required'}, status=400)

        exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
        exchange_response = client.item_public_token_exchange(exchange_request)

        # Save the access token and item ID to the database
        access_token = exchange_response.access_token
        item_id = exchange_response.item_id

        if request.user.is_authenticated:
            # Save to PlaidItem associated with the user
            plaid_item, created = PlaidItem.objects.get_or_create(user=request.user)
            plaid_item.access_token = access_token
            plaid_item.item_id = item_id
            plaid_item.save()
        else:
            # Handle unauthenticated users
            pass  # Implement your logic here

        return JsonResponse({'access_token': access_token})

    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as general_error:
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)
    

@csrf_exempt
def get_account_balances(request):
    client = get_plaid_client()

    try:
        # Retrieve the stored access token for the user
        plaid_item = PlaidItem.objects.get(user=request.user)
        access_token = plaid_item.access_token

        accounts_request = AccountsBalanceGetRequest(access_token=access_token)
        accounts_response = client.accounts_balance_get(accounts_request)
        return JsonResponse(accounts_response.to_dict())
    except PlaidItem.DoesNotExist:
        return JsonResponse({'error': 'Access token not found for user'}, status=400)
    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)
