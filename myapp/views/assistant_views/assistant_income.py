from myapp.models import IncomeRecord, User
from django.http import JsonResponse
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404
import re

def handle_income_action(action_data, user_id):
    if not user_id:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    user = get_object_or_404(User, id=user_id)

    action = action_data.get('action')
    title = action_data.get('name')
    amount = action_data.get('amount')
    record_date = action_data.get('record_date')

    if action == 'add_income':
        if not title or not amount or not record_date:
            return JsonResponse({'error': 'Title, amount, and date are required to add an income record.'}, status=400)

        clean_amount = re.sub(r'[^\d.-]', '', amount)
        try:
            amount_decimal = Decimal(clean_amount)
            record_date_parsed = parse_date(record_date)
        except (InvalidOperation, ValueError) as e:
            return JsonResponse({'error': str(e)}, status=400)

        IncomeRecord.objects.create(
            user=user,
            title=title,
            amount=amount_decimal,
            record_date=record_date_parsed
        )

        update_income_by_periods(user)
        return JsonResponse({'reply': f'Income record "{title}" added successfully!'}, status=200)

    elif action == 'list_income':
        income_records = IncomeRecord.objects.filter(user=user).order_by('-record_date')
        if not income_records.exists():
            return JsonResponse({'reply': 'You have no income records.'}, status=200)

        reply = "Here are your income records:\n"
        for record in income_records:
            reply += f"- {record.title}: {record.amount} on {record.record_date}\n"
        return JsonResponse({'reply': reply}, status=200)

    else:
        return JsonResponse({'error': 'Invalid action specified.'}, status=400)

def update_income_by_periods(user):
    now = datetime.now()
    current_week_start = now - timedelta(days=now.weekday())
    current_month = now.month
    current_year = now.year

    weekly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__gte=current_week_start
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    monthly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__year=current_year,
        record_date__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    yearly_income = IncomeRecord.objects.filter(
        user=user,
        record_date__year=current_year
    ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    user.income_by_week = weekly_income
    user.income_by_month = monthly_income
    user.income_by_year = yearly_income
    user.save()

def parse_date(date_str):
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d.%m.%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError("Invalid date format. Please use YYYY-MM-DD, MM/DD/YYYY, or DD.MM.YYYY.")