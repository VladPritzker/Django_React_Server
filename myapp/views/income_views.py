from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime
from myapp.models import IncomeRecord, User
from django.shortcuts import get_object_or_404
from decimal import Decimal
from datetime import datetime, timedelta
from django.db.models import Sum





@csrf_exempt
def income_records_view(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)

        if request.method == 'GET':
            income_records = IncomeRecord.objects.filter(user=user).order_by('-record_date')
            records = [
                {
                    'id': record.id,
                    'title': record.title,
                    'amount': str(record.amount),
                    'record_date': record.record_date.isoformat()
                } for record in income_records
            ]
            return JsonResponse(records, safe=False, status=200)    

        elif request.method == 'POST':
            data = json.loads(request.body)
            title = data.get('title')
            amount = data.get('amount')
            record_date = data.get('record_date')

            if not title or not amount or not record_date:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            record_date = datetime.strptime(record_date, '%Y-%m-%d').date()

            record = IncomeRecord.objects.create(
                user=user,
                title=title,
                amount=amount,
                record_date=record_date
            )
            
            update_income_by_periods(user)
            return JsonResponse({
                'id': record.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat()
            }, status=201)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def income_record_detail_view(request, user_id, record_id):
    if request.method == 'DELETE':
        try:
            user = get_object_or_404(User, id=user_id)
            income_record = get_object_or_404(IncomeRecord, id=record_id, user=user)

            user.balance -= Decimal(income_record.amount)
            user.save()

            income_record.delete()

            update_income_by_periods(user)

            return JsonResponse({'message': 'Income record deleted successfully'}, status=200)
        except IncomeRecord.DoesNotExist:
            return JsonResponse({'error': 'Income record not found'}, status=404)

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

