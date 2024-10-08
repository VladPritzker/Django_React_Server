import json
import uuid
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from plaid.rest import ApiException

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from django.utils.decorators import method_decorator


from myapp.models import PlaidItem
from django.contrib.auth.decorators import login_required

# Initialize Plaid client with credentials from Django settings
configuration = Configuration(
    host=settings.PLAID_HOST,
    api_key={
        'clientId': settings.PLAID_CLIENT_ID,
        'secret': settings.PLAID_SECRET
    }
)

api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)  # Correct client initialization

@csrf_exempt
def create_link_token(request):
    if request.method == 'POST':
        try:
            # Generate a unique client_user_id for the request
            user_id = str(uuid.uuid4())

            # Create the Link Token request payload
            request_payload = LinkTokenCreateRequest(
                products=[Products("transactions")],
                client_name="Your App",
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=user_id)
            )
            # Send request to Plaid API to create link token
            response = plaid_client.link_token_create(request_payload)
            return JsonResponse({'link_token': response['link_token']}, status=200)
        
        except ApiException as e:
            # Handle any API errors
            error_message = json.loads(e.body).get('error_message', 'Error creating link token.')
            return JsonResponse({'error': error_message}, status=500)
        
        except Exception as e:
            # Handle any other unexpected errors
            return JsonResponse({'error': str(e)}, status=500)

    # If the request method is not POST, return a Method Not Allowed response
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
def exchange_public_token(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'User is not authenticated.'}, status=403)

            data = json.loads(request.body)
            public_token = data.get('public_token')
            
            # Create a request to exchange the public token for an access token
            exchange_request = ItemPublicTokenExchangeRequest(public_token=public_token)
            exchange_response = plaid_client.item_public_token_exchange(exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']

            # Save access_token and item_id in the database for future use
            plaid_item, created = PlaidItem.objects.get_or_create(user=request.user)
            plaid_item.access_token = access_token
            plaid_item.item_id = item_id
            plaid_item.save()

            return JsonResponse({'message': 'Access token retrieved successfully.'}, status=200)
        except ApiException as e:
            error_message = json.loads(e.body).get('error_message', 'Unable to exchange public token')
            return JsonResponse({'error': error_message}, status=500)


@csrf_exempt
def get_account_data(request):
    try:
        user_id = request.user.id
        plaid_item = PlaidItem.objects.get(user_id=user_id)
        access_token = plaid_item.access_token

        balance_request = AccountsBalanceGetRequest(access_token=access_token)
        balance_response = plaid_client.accounts_balance_get(balance_request)

        return JsonResponse({'accounts': balance_response.to_dict()}, status=200)
    except PlaidItem.DoesNotExist:
        return JsonResponse({'error': 'Plaid item not found for user'}, status=404)
    except ApiException as e:
        error_message = json.loads(e.body).get('error_message', 'Error retrieving account data.')
        return JsonResponse({'error': error_message}, status=500)
