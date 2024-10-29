from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from myapp.models import PlaidItem, FinancialRecord
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

        # Create a mapping from account_id to account_name
        account_id_to_name = {account.account_id: account.name for account in accounts}
        logger.info(f"Account ID to Name Mapping: {account_id_to_name}")

        # Handle TRANSACTIONS webhooks
        if webhook_type == "TRANSACTIONS" and webhook_code in [
            "INITIAL_UPDATE",
            "HISTORICAL_UPDATE",
            "DEFAULT_UPDATE",
            "SYNC_UPDATES_AVAILABLE",
        ]:
            # Fetch new transactions using the transactions_sync endpoint
            cursor = plaid_item.cursor  # May be None initially
            has_more = True

            while has_more:
                # Prepare request options if needed
                request_options = TransactionsSyncRequestOptions(
                    include_personal_finance_category=True
                )

                # Prepare the TransactionsSyncRequest
                if cursor is not None:
                    sync_request = TransactionsSyncRequest(
                        access_token=access_token,
                        cursor=cursor,
                        count=100,
                        options=request_options
                    )
                else:
                    sync_request = TransactionsSyncRequest(
                        access_token=access_token,
                        count=100,
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

                    # Get the account name using the mapping
                    target_account_id = 'dOjAOoNZQyi59qLaYAp8uEgnBdNAKMHjxZY74'

                    # Check if the transaction is from the specified card
                    if account_id == target_account_id:
                        # Check if transaction_id already exists
                        if not FinancialRecord.objects.filter(user=user, transaction_id=transaction_id).exists():
                            # Treat all amounts as expenses and store as positive
                            positive_amount = abs(amount)

                            # Save to FinancialRecord
                            FinancialRecord.objects.create(
                                user=user,
                                title=title,
                                amount=positive_amount,
                                record_date=record_date,
                                transaction_id=transaction_id
                            )

                            # Update user's balance
                            user.balance -= positive_amount  # Subtract the amount from balance
                            user.save()
                        else:
                            logger.info(f"Transaction {transaction_id} already exists. Skipping.")

                # Process modified and removed transactions if necessary (optional)

                # Update the cursor
                cursor = sync_response.next_cursor
                plaid_item.cursor = cursor
                plaid_item.save()

                has_more = sync_response.has_more

            # Update user's spending after processing transactions
            update_spending_by_periods(user)

            return JsonResponse({"status": "success"}, status=200)
        else:
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


def update_income_by_periods(user, skip_update=False):
    if skip_update:
        return

    now = datetime.now()
    current_week_start = now - timedelta(days=now.weekday())  # Start of the week (Monday)
    current_month = now.month
    current_year = now.year

    # Calculate income for the current week
    weekly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__gte=current_week_start
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Calculate income for the current month
    monthly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__year=current_year,
        record_date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Calculate income for the current year
    yearly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # Update the user's income_by_week, income_by_month, and income_by_year fields
    user.income_by_week = weekly_income
    user.income_by_month = monthly_income
    user.income_by_year = yearly_income
    user.save()
