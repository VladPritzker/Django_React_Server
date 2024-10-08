from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from plaid.api import plaid_api
from plaid.rest import ApiException
from plaid.models import AccountsBalanceGetRequest, TransactionsGetRequest, TransactionsGetRequestOptions
from datetime import datetime, timedelta
from django.conf import settings
from myapp.models import PlaidItem
from myapp.views.plaid.plaid_helpers import plaid_client
from django.contrib.auth.decorators import login_required

@csrf_exempt
def get_account_data(request):
    try:
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated.'}, status=403)

        # Retrieve the access token for the authenticated user from the database
        user_id = request.user.id
        plaid_item = PlaidItem.objects.get(user_id=user_id)
        access_token = plaid_item.access_token

        # Initialize Plaid client
        client = get_plaid_client()

        # Use access token to get account balances
        request_data = AccountsBalanceGetRequest(access_token=access_token)
        response = client.accounts_balance_get(request_data)

        # Return the response to the frontend
        return JsonResponse(response.to_dict(), safe=False)

    except PlaidItem.DoesNotExist:
        return JsonResponse({'error': 'Access token not found for user.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_transaction_data(request):
    try:
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User is not authenticated.'}, status=403)

        user_id = request.user.id
        plaid_item = PlaidItem.objects.get(user_id=user_id)
        access_token = plaid_item.access_token

        # Initialize Plaid client
        client = get_plaid_client()

        # Set a date range for the transactions
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Use access token to get transaction data
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options=TransactionsGetRequestOptions(count=100)
        )
        response = client.transactions_get(request_data)

        # Return the response to the frontend
        return JsonResponse(response.to_dict(), safe=False)

    except PlaidItem.DoesNotExist:
        return JsonResponse({'error': 'Access token not found for user.'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
