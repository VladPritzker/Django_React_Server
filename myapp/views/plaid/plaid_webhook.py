from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import FinancialRecord, User
from datetime import datetime
from decimal import Decimal
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

        # Check for new transactions
        if webhook_type == "TRANSACTIONS" and webhook_code == "DEFAULT_UPDATE":
            user = get_object_or_404(User, plaid_item_id=item_id)
            transactions = data.get("new_transactions", [])

            # Store each new transaction as a FinancialRecord
            for transaction in transactions:
                record = FinancialRecord.objects.create(
                    user=user,
                    title=transaction.get("name"),
                    amount=Decimal(transaction.get("amount")),
                    record_date=datetime.strptime(transaction.get("date"), '%Y-%m-%d')
                )

                # Update user's balance
                user.balance -= record.amount
                user.save()

                # Update spending summary by period
                update_spending_by_periods(user)

            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "ignored"}, status=200)

    except Exception as e:
        logger.error(f"Error processing Plaid webhook: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
