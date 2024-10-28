# webhook.py
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import FinancialRecord, PlaidItem
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
        # Parse the webhook payload
        data = json.loads(request.body)
        webhook_type = data.get("webhook_type")
        webhook_code = data.get("webhook_code")
        item_id = data.get("item_id")
        logger.info(f"Received webhook for item_id: {item_id}, type: {webhook_type}, code: {webhook_code}")

        # Find the associated PlaidItem and user using item_id
        plaid_item = get_object_or_404(PlaidItem, item_id=item_id)
        user = plaid_item.user
        access_token = plaid_item.access_token  # Retrieve the access token

        # Handle TRANSACTIONS webhooks
        if webhook_type == "TRANSACTIONS" and webhook_code in ["INITIAL_UPDATE", "HISTORICAL_UPDATE", "DEFAULT_UPDATE"]:
            # Fetch new transactions using the transactions_sync endpoint
            cursor = plaid_item.cursor  # May be None initially
            has_more = True

            while has_more:
                request_options = TransactionsSyncRequestOptions(count=100)
                # Conditionally include 'cursor' only if it's not None
                if cursor:
                    sync_request = TransactionsSyncRequest(
                        access_token=access_token,
                        cursor=cursor,
                        options=request_options
                    )
                else:
                    sync_request = TransactionsSyncRequest(
                        access_token=access_token,
                        options=request_options
                    )
                sync_response = plaid_client.transactions_sync(sync_request)

                # Process added transactions
                for transaction in sync_response.added:
                    # Save each transaction to the FinancialRecord model
                    FinancialRecord.objects.update_or_create(
                        transaction_id=transaction.transaction_id,
                        defaults={
                            'user': user,
                            'title': transaction.name,
                            'amount': Decimal(transaction.amount),
                            'record_date': datetime.strptime(transaction.date, '%Y-%m-%d'),
                            # Add other fields as necessary
                        }
                    )

                    # Update user's balance
                    user.balance -= Decimal(transaction.amount)
                    user.save()

                # Process modified transactions (optional)
                for transaction in sync_response.modified:
                    # Update existing transactions
                    FinancialRecord.objects.update_or_create(
                        transaction_id=transaction.transaction_id,
                        defaults={
                            'user': user,
                            'title': transaction.name,
                            'amount': Decimal(transaction.amount),
                            'record_date': datetime.strptime(transaction.date, '%Y-%m-%d'),
                            # Update other fields as necessary
                        }
                    )

                # Process removed transactions
                for removed_transaction in sync_response.removed:
                    FinancialRecord.objects.filter(transaction_id=removed_transaction.transaction_id).delete()

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
    current_week_start = now - timedelta(days=(now.weekday() + 1) % 7)  # Start of the week (Sunday)
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