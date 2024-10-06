# In views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def exchange_public_token(request):
    client = get_plaid_client()
    data = json.loads(request.body)
    public_token = data.get('public_token')
    
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']
    item_id = exchange_response['item_id']
    
    # Store the access_token securely in your database
    # Example: Assuming you have a model to store Plaid access tokens
    plaid_item = PlaidItem.objects.create(
        user=request.user,
        access_token=access_token,
        item_id=item_id
    )
    
    return JsonResponse({'status': 'success'})


# In views.py
def get_account_balances(request):
    client = get_plaid_client()
    # Retrieve the stored access token for the user
    plaid_item = PlaidItem.objects.get(user=request.user)
    access_token = plaid_item.access_token
    
    # Fetch account balances using the access token
    accounts_response = client.Accounts.balance.get(access_token)
    return JsonResponse(accounts_response)
