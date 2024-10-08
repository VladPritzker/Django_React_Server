# assistant_income.py

from myapp.models import IncomeRecord, User
from django.http import JsonResponse
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404

def handle_income_action(action_data, user_id):
    if not user_id:
        return JsonResponse({'error': 'User ID is missing'}, status=400)
    
    # Retrieve the user
    user = get_object_or_404(User, id=user_id)

    action = action_data.get('action')
    title = action_data.get('name')  # Using 'name' for income title
    amount = action_data.get('amount')
    record_date = action_data.get('record_date')
    
    if not title or not amount or not record_date:
        return JsonResponse({'error': 'Title, amount, and date are required to add an income record.'}, status=400)
    elif not record_date:
        return JsonResponse({'warning': 'Please include a date when adding income or spending.'}, status=400)
    if action == 'add_income':

        try:
            # Parse amount and date
            amount = Decimal(amount)
            record_date = datetime.strptime(record_date, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid amount or date format. Date should be YYYY-MM-DD.'}, status=400)
        # Create a new income record
        record = IncomeRecord.objects.create(
            user=user,
            title=title,
            amount=amount,
            record_date=record_date
        )
        # Update income summaries
        update_income_by_periods(user)
        return JsonResponse({'reply': f'Income record "{title}" added successfully!'}, status=200)    
    elif action == 'list_income':
        # Fetch the income records for the user
        income_records = IncomeRecord.objects.filter(user=user).order_by('-record_date')
        if not income_records.exists():
            return JsonResponse({'reply': 'You have no income records.'}, status=200)
        # Format the income records into a string
        reply = "Here are your income records:\n"
        for record in income_records:
            reply += f"- {record.title}: {record.amount} on {record.record_date}\n"
        return JsonResponse({'reply': reply}, status=200)
    else:
        return JsonResponse({'error': 'Invalid action specified.'}, status=400)

def update_income_by_periods(user):
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
