# In views.py
def get_account_balances(request):
    client = get_plaid_client()
    # Retrieve the stored access token for the user
    plaid_item = PlaidItem.objects.get(user=request.user)
    access_token = plaid_item.access_token
    
    # Fetch account balances using the access token
    accounts_response = client.Accounts.balance.get(access_token)
    return JsonResponse(accounts_response)
