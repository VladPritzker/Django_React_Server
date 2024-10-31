from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from myapp.models import PlaidItem, FinancialRecord, TrackedAccount
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions
from .plaid_client import plaid_client
from .plaid_views import get_account_data_util  # Import the utility function
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def plaid_webhook(request):
    try:
        # Read and log the raw request body
        raw_body = request.body.decode('utf-8')
        logger.info(f"Received webhook raw body: {raw_body}")

        # Parse the webhook payload
        data = json.loads(raw_body)

        # Optionally, log the parsed JSON data
        logger.info(f"Received webhook JSON data: {json.dumps(data)}")

        webhook_type = data.get("webhook_type")
        webhook_code = data.get("webhook_code")
        item_id = data.get("item_id")
        logger.info(f"Received webhook for item_id: {item_id}, type: {webhook_type}, code: {webhook_code}")

        # Find the associated PlaidItem using item_id or previous_item_id
        try:
            plaid_item = PlaidItem.objects.get(Q(item_id=item_id) | Q(previous_item_id=item_id))
        except PlaidItem.DoesNotExist:
            logger.warning(f"PlaidItem with item_id {item_id} not found. Webhook will be ignored.")
            return JsonResponse({"status": "item_not_found"}, status=200)

        user = plaid_item.user
        access_token = plaid_item.access_token  # Retrieve the access token

        # Fetch account data once outside the loop
        accounts = get_account_data_util(access_token)
        if accounts is None:
            logger.error("Failed to retrieve account data.")
            return JsonResponse({"error": "Failed to retrieve account data."}, status=500)

        # Create a mapping from account_id to account info (name and mask)
        account_id_to_info = {
            account.account_id: {
                'name': account.name,
                'mask': account.mask
            }
            for account in accounts
        } 
        logger.info(f"Account ID to Info Mapping: {account_id_to_info}")

        # Get user's tracked accounts
        tracked_accounts = TrackedAccount.objects.filter(user=user).values_list('account_id', flat=True)
        tracked_account_ids = set(tracked_accounts)

        logger.info(f"User's tracked account IDs: {tracked_account_ids}")

        # Handle only SYNC_UPDATES_AVAILABLE webhook
        # if webhook_type == "TRANSACTIONS" and webhook_code == "SYNC_UPDATES_AVAILABLE":
        if webhook_type == "TRANSACTIONS" and webhook_code in ["INITIAL_UPDATE", "HISTORICAL_UPDATE", "SYNC_UPDATES_AVAILABLE"]:

            # Fetch new transactions using the transactions_sync endpoint
            cursor = plaid_item.cursor  # May be None initially
            has_more = True

            while has_more:
                # Prepare request options if needed
                request_options = TransactionsSyncRequestOptions(
                    include_personal_finance_category=True
                )

                # Prepare the TransactionsSyncRequest
                sync_request = TransactionsSyncRequest(
                    access_token=access_token,
                    cursor=cursor,
                    options=request_options
                )

                # Make the API call
                sync_response = plaid_client.transactions_sync(sync_request)

                # Process added transactions
                for transaction in sync_response.added:
                    amount = Decimal(transaction.amount)
                    transaction_id = transaction.transaction_id
                    record_date = transaction.date
                    title = transaction.name
                    account_id = transaction.account_id

                    # Get the account info using the mapping
                    account_info = account_id_to_info.get(account_id, {})
                    account_name = account_info.get('name', '')
                    account_mask = account_info.get('mask', '')

                    logger.info(f"Evaluating transaction {transaction_id}: account_name='{account_name}', account_mask='{account_mask}'")

                    # Check if the account is in the user's tracked accounts
                    if account_id in tracked_account_ids:
                        logger.info(f"Processing transaction {transaction_id} from tracked account.")
                        # Use update_or_create to prevent duplicates
                        FinancialRecord.objects.update_or_create(
                            user=user,
                            transaction_id=transaction_id,
                            defaults={
                                'title': title,
                                'amount': abs(amount),
                                'record_date': record_date,
                            }
                        )

                        # Update user's balance
                        user.balance -= abs(amount)  # Subtract the amount from balance
                        user.save()
                    else:
                        logger.info(f"Ignoring transaction {transaction_id} from account {account_name} ending with {account_mask}")

                # Update the cursor
                cursor = sync_response.next_cursor
                plaid_item.cursor = cursor
                plaid_item.save()

                has_more = sync_response.has_more

            # Update user's spending after processing transactions
            update_spending_by_periods(user)

            return JsonResponse({"status": "success"}, status=200)
        else:
            logger.info(f"Ignoring webhook with code: {webhook_code}")
            return JsonResponse({"status": "ignored"}, status=200)

    except Exception as e:
        logger.error(f"Error processing Plaid webhook: {str(e)}", exc_info=True)
        return JsonResponse({"error": str(e)}, status=500)

def update_spending_by_periods(user, skip_update=False):
    if skip_update:
        return

    now = datetime.now()
    current_week_start = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    current_month = now.month
    current_year = now.year

    # Calculate spending for the current week
    weekly_spending = FinancialRecord.objects.filter(
        user=user,
        record_date__gte=current_week_start
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Calculate spending for the current month
    monthly_spending = FinancialRecord.objects.filter(
        user=user,
        record_date__year=current_year,
        record_date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Calculate spending for the current year
    yearly_spending = FinancialRecord.objects.filter(
        user=user,
        record_date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Update the user's spent_by_week, spent_by_month, and spent_by_year fields
    user.spent_by_week = weekly_spending
    user.spent_by_month = monthly_spending
    user.spent_by_year = yearly_spending
    user.save()
