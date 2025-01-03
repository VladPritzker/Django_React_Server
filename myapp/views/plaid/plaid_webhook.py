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
        webhook_type = data.get("webhook_type")
        webhook_code = data.get("webhook_code")
        item_id = data.get("item_id")

        # Retrieve the associated PlaidItem
        try:
            plaid_item = PlaidItem.objects.get(Q(item_id=item_id) | Q(previous_item_id=item_id))
        except PlaidItem.DoesNotExist:
            logger.warning(f"PlaidItem with item_id {item_id} not found. Webhook will be ignored.")
            return JsonResponse({"status": "item_not_found"}, status=200)

        user = plaid_item.user
        access_token = plaid_item.access_token

        # Fetch account data
        accounts = get_account_data_util(access_token)
        if accounts is None:
            logger.error("Failed to retrieve account data.")
            return JsonResponse({"error": "Failed to retrieve account data."}, status=500)

        # Create account mapping
        account_id_to_info = {
            account.account_id: {
                'name': account.name,
                'mask': account.mask
            }
            for account in accounts
        }
        tracked_accounts = TrackedAccount.objects.filter(user=user).values_list('account_id', flat=True)
        tracked_account_ids = set(tracked_accounts)

        # Define phrases to exclude
        exclude_phrases = ["Online payment from", "PENDING PAYMENT"]

        # Process transaction updates
        if webhook_type == "TRANSACTIONS" and webhook_code in ["INITIAL_UPDATE", "HISTORICAL_UPDATE", "SYNC_UPDATES_AVAILABLE"]:
            cursor = plaid_item.cursor  # May be None initially
            has_more = True

            while has_more:
                request_options = TransactionsSyncRequestOptions(
                    include_personal_finance_category=True
                )

                # Conditionally include cursor
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

                # Make the API call
                sync_response = plaid_client.transactions_sync(sync_request)

                # Process added transactions
                for transaction in sync_response.added:
                    amount = Decimal(transaction.amount)
                    transaction_id = transaction.transaction_id
                    record_date = transaction.date
                    title = transaction.name
                    account_id = transaction.account_id
                    pending = transaction.pending
                    pending_id = getattr(transaction, 'pending_transaction_id', None)

                    # Get account info
                    account_info = account_id_to_info.get(account_id, {})
                    account_name = account_info.get('name', '')
                    account_mask = account_info.get('mask', '')

                    logger.info(f"Evaluating transaction {transaction_id}: account_name='{account_name}', account_mask='{account_mask}', pending={pending}")

                    # Skip excluded phrases
                    if any(phrase in title for phrase in exclude_phrases):
                        logger.info(f"Skipping transaction {transaction_id} with title '{title}' due to exclude phrases")
                        continue

                    # Skip pending transactions to avoid duplicates
                    if pending:
                        logger.info(f"Skipping pending transaction {transaction_id}")
                        continue

                    # Now we deal with final transactions
                    if account_id in tracked_account_ids:
                        logger.info(f"Processing final transaction {transaction_id} from tracked account.")

                        # If this final transaction references a pending one
                        if pending_id:
                            # Try updating a record created by that pending transaction_id
                            updated = FinancialRecord.objects.filter(
                                user=user, transaction_id=pending_id
                            ).update(
                                transaction_id=transaction_id,
                                title=title,
                                amount=abs(amount),
                                record_date=record_date
                            )
                            if updated:
                                logger.info(f"Updated record from pending {pending_id} to final {transaction_id}")
                                # If you never saved pending transactions before, updated will be 0, so it won't happen.
                                # If updated, you might have already adjusted balance at pending stage (if you did so), otherwise adjust now.
                                # If you never adjusted at pending stage, adjust now:
                                # If you did adjust at pending stage, no double-adjust needed.
                                # For simplicity, assume we never adjusted pending stage, so adjust now:
                                if updated == 1:
                                    user.balance -= abs(amount)
                                    user.save()
                                continue

                        # If no pending_id or no update happened, treat this as a new final transaction
                        _, created = FinancialRecord.objects.update_or_create(
                            user=user,
                            transaction_id=transaction_id,
                            defaults={
                                'title': title,
                                'amount': abs(amount),
                                'record_date': record_date,
                            }
                        )
                        if created:
                            user.balance -= abs(amount)
                            user.save()
                    else:
                        logger.info(f"Ignoring transaction {transaction_id} from account {account_name} ending with {account_mask}")

                # Update cursor and save
                cursor = sync_response.next_cursor
                plaid_item.cursor = cursor
                plaid_item.save()

                has_more = sync_response.has_more

            # Update user's spending
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
