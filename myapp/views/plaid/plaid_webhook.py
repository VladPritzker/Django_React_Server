from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from myapp.models import FinancialRecord, PlaidItem, IncomeRecord
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_sync_request_options import TransactionsSyncRequestOptions
from .plaid_client import plaid_client
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
                    record_date = transaction.date  # Assuming this is a string in 'YYYY-MM-DD' format
                    title = transaction.name

                    # Check if the transaction is income or expense
                    if amount > 0:
                        # Income transaction
                        # Save to IncomeRecord
                        IncomeRecord.objects.update_or_create(
                            transaction_id=transaction_id,
                            defaults={
                                'user': user,
                                'title': title,
                                'amount': amount,
                                'record_date': record_date,
                                # Add other fields as necessary
                            }
                        )
                        # Update user's balance
                        user.balance += amount
                        user.save()
                    else:
                        # Expense transaction
                        positive_amount = abs(amount)  # Convert to positive value
                        # Save to FinancialRecord
                        FinancialRecord.objects.update_or_create(
                            transaction_id=transaction_id,
                            defaults={
                                'user': user,
                                'title': title,
                                'amount': positive_amount,  # Store as positive value
                                'record_date': record_date,
                                # Add other fields as necessary
                            }
                        )
                        # Update user's balance
                        user.balance += amount  # amount is negative, so this subtracts from balance
                        user.save()

                # Process modified transactions (optional)
                for transaction in sync_response.modified:
                    amount = Decimal(transaction.amount)
                    transaction_id = transaction.transaction_id
                    record_date = transaction.date
                    title = transaction.name

                    # Determine if transaction exists in IncomeRecord or FinancialRecord
                    income_exists = IncomeRecord.objects.filter(transaction_id=transaction_id).exists()
                    expense_exists = FinancialRecord.objects.filter(transaction_id=transaction_id).exists()

                    if amount > 0:
                        # Income transaction
                        if expense_exists:
                            # Remove from FinancialRecord
                            expense = FinancialRecord.objects.get(transaction_id=transaction_id)
                            user.balance += Decimal(expense.amount)  # Reverse the expense
                            expense.delete()

                        # Update or create in IncomeRecord
                        IncomeRecord.objects.update_or_create(
                            transaction_id=transaction_id,
                            defaults={
                                'user': user,
                                'title': title,
                                'amount': amount,
                                'record_date': record_date,
                            }
                        )
                        # Update user's balance
                        user.balance += amount
                        user.save()
                    else:
                        # Expense transaction
                        positive_amount = abs(amount)
                        if income_exists:
                            # Remove from IncomeRecord
                            income = IncomeRecord.objects.get(transaction_id=transaction_id)
                            user.balance -= Decimal(income.amount)  # Reverse the income
                            income.delete()

                        # Update or create in FinancialRecord
                        FinancialRecord.objects.update_or_create(
                            transaction_id=transaction_id,
                            defaults={
                                'user': user,
                                'title': title,
                                'amount': positive_amount,  # Store as positive value
                                'record_date': record_date,
                            }
                        )
                        # Update user's balance
                        user.balance += amount  # amount is negative
                        user.save()

                # Process removed transactions
                for removed_transaction in sync_response.removed:
                    transaction_id = removed_transaction.transaction_id
                    # Remove from IncomeRecord if exists
                    if IncomeRecord.objects.filter(transaction_id=transaction_id).exists():
                        income = IncomeRecord.objects.get(transaction_id=transaction_id)
                        user.balance -= Decimal(income.amount)
                        income.delete()
                    # Remove from FinancialRecord if exists
                    elif FinancialRecord.objects.filter(transaction_id=transaction_id).exists():
                        expense = FinancialRecord.objects.get(transaction_id=transaction_id)
                        user.balance += Decimal(expense.amount)  # amount stored as positive
                        expense.delete()
                    user.save()

                # Update the cursor
                cursor = sync_response.next_cursor
                plaid_item.cursor = cursor
                plaid_item.save()

                has_more = sync_response.has_more

            # Update user's spending and income after processing transactions
            update_spending_by_periods(user)
            update_income_by_periods(user)

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
