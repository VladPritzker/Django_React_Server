#  webhook file
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import FinancialRecord, User, PlaidItem
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from .plaid_client import plaid_client


import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

from plaid.model.transactions_refresh_request import TransactionsRefreshRequest

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

        # Find the associated user using item_id
        plaid_item = get_object_or_404(PlaidItem, item_id=item_id)
        user = plaid_item.user
        access_token = plaid_item.access_token  # Retrieve the access token

        # Trigger transaction refresh when specific webhook codes are received
        if webhook_type == "TRANSACTIONS" and webhook_code == "DEFAULT_UPDATE":
            # Call transactions/refresh to request Plaid to check for new transactions
            refresh_request_data = TransactionsRefreshRequest(access_token=access_token)
            plaid_client.transactions_refresh(refresh_request_data)

            transactions = data.get("new_transactions", [])

            # Store each transaction as a FinancialRecord
            for transaction in transactions:
                record = FinancialRecord.objects.create(
                    user=user,
                    title=transaction.get("name"),
                    amount=Decimal(transaction.get("amount")),
                    record_date=datetime.strptime(transaction.get("date"), '%Y-%m-%d')
                )

                # Update the user's balance and spending
                user.balance -= record.amount
                user.save()
                update_spending_by_periods(user)

            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "ignored"}, status=200)
    except Exception as e:
        logger.error(f"Error processing Plaid webhook: {str(e)}")
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