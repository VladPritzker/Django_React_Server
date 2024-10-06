from plaid.models import LinkTokenCreateRequest, ItemPublicTokenExchangeRequest, CountryCode
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from plaid.api import plaid_api
from plaid.api_client import ApiClient
from plaid.configuration import Configuration
from plaid.rest import ApiException
from django.conf import settings
import json
from myapp.models import PlaidItem  # Import your PlaidItem model
from plaid.models import ItemPublicTokenExchangeRequest



def get_plaid_client():
    configuration = Configuration(
        host=settings.PLAID_HOST,
        api_key={
            'clientId': settings.PLAID_CLIENT_ID,
            'secret': settings.PLAID_SECRET
        }
    )
    api_client = ApiClient(configuration)
    plaid_client = plaid_api.PlaidApi(api_client)
    return plaid_client


@csrf_exempt
def create_link_token(request):
    client = get_plaid_client()
    try:
        # Correct usage of CountryCode enum
        request_data = link_token_create_request.LinkTokenCreateRequest(
            products=['transactions'],
            client_name="Your App",
            country_codes=[CountryCode.US],  # Use CountryCode.US instead of 'US'
            language='en',
            user={
                'client_user_id': str(request.user.id)  # Make sure request.user is authenticated
            }
        )
        response = client.link_token_create(request_data)
        return JsonResponse({'link_token': response['link_token']})
    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def create_link_token(request):
    client = get_plaid_client()
    try:
        request_data = LinkTokenCreateRequest(
            products=['transactions'],
            client_name="Your App",
            country_codes=[CountryCode.US],  # Correct usage of CountryCode
            language='en',
            user={
                'client_user_id': str(request.user.id)  # Make sure request.user is authenticated
            }
        )
        response = client.link_token_create(request_data)
        return JsonResponse({'link_token': response['link_token']})
    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def get_account_balances(request):
    client = get_plaid_client()
    
    try:
        # Retrieve the stored access token for the user
        plaid_item = PlaidItem.objects.get(user=request.user)
        access_token = plaid_item.access_token
        
        # Fetch account balances using the access token
        accounts_response = client.accounts_balance_get(access_token)
        return JsonResponse(accounts_response.to_dict())
    except PlaidItem.DoesNotExist:
        return JsonResponse({'error': 'Access token not found for user'}, status=400)
    except ApiException as e:
        return JsonResponse({'error': str(e)}, status=400)


def exchange_public_token(public_token):
    # Initialize Plaid client
    client = get_plaid_client()
    # Exchange the public token for an access token
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = client.item_public_token_exchange(request)
    return response['access_token']
