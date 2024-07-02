from django.views.decorators.http import require_http_methods  # Add this import
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import FinancialRecord, User
import json
from datetime import datetime, timedelta
from decimal import Decimal
from django.db.models import Sum

def update_spending_by_periods(user):
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

@csrf_exempt
def financial_records(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            title = data.get('title')
            amount = Decimal(data.get('amount'))
            record_date = data.get('record_date')

            parsed_date = datetime.strptime(record_date, '%Y-%m-%d').date()
            user = User.objects.get(id=user_id)

            record = FinancialRecord.objects.create(
                user=user,
                title=title,
                amount=amount,
                record_date=parsed_date
            )
            
            user.balance -= amount
            user.save()

            update_spending_by_periods(user)

            return JsonResponse({
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat()
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as ve:
            return JsonResponse({'error': 'Date format error: ' + str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        records = FinancialRecord.objects.all()
        if user_id:
            records = records.filter(user_id=user_id)

        records_data = [
            {'id': record.id, 'user_id': record.user.id, 'record_date': record.record_date.isoformat(),
             'title': record.title, 'amount': float(record.amount)}
            for record in records
        ]
        return JsonResponse(records_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_financial_record(request, user_id, record_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            record = FinancialRecord.objects.get(id=record_id, user=user)
            
            user.balance += record.amount
            user.save()
            
            record.delete()

            update_spending_by_periods(user)

            return JsonResponse({'message': 'Record deleted successfully'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except FinancialRecord.DoesNotExist:
            return JsonResponse({'error': 'Financial record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
