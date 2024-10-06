# In views.py
from django.http import JsonResponse
from plaid.model import LinkTokenCreateRequest
from plaid.api import plaid_api
import plaid

def create_link_token(request):
    client = get_plaid_client()
    request_data = LinkTokenCreateRequest(
        products=[plaid.Product.TRANSACTIONS],
        client_name="Your App",
        country_codes=['US'],
        language='en',
        user={
            'client_user_id': str(request.user.id)  # Use the user’s ID or any unique identifier
        }
    )
    
    response = client.link_token_create(request_data)
    return JsonResponse({'link_token': response['link_token']})
