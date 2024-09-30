from myapp.models import FinancialRecord, User
from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime
from django.db.models import Sum
from datetime import datetime, timedelta


# Function to handle spending actions
def handle_spending_action(action_data, user_id):
    if not user_id:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    action = action_data.get('action')
    title = action_data.get('name')
    amount = action_data.get('amount')
    record_date = action_data.get('record_date')

    if action == 'add_spending':
        if not title or not amount or not record_date:
            return JsonResponse({'error': 'Title, amount, and date are required to add spending.'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            parsed_date = datetime.strptime(record_date, '%Y-%m-%d').date()
            amount_decimal = Decimal(amount)

            record = FinancialRecord.objects.create(
                user=user,
                title=title,
                amount=amount_decimal,
                record_date=parsed_date
            )

            user.balance -= amount_decimal
            user.save()

            update_spending_by_periods(user)

            return JsonResponse({'reply': f'Spending "{title}" of ${amount} added successfully!'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

    elif action == 'list_spending':
        try:
            user = User.objects.get(id=user_id)
            spendings = FinancialRecord.objects.filter(user=user)

            if not spendings.exists():
                return JsonResponse({'reply': 'You have no spending records.'}, status=200)

            reply = "Here are your spendings:\n"
            for spending in spendings:
                reply += f"- {spending.title}: ${spending.amount} on {spending.record_date}\n"

            return JsonResponse({'reply': reply}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


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