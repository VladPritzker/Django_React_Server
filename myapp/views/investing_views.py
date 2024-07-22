from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import InvestingRecord, User
import json
from datetime import datetime, timedelta
from decimal import Decimal
import numpy as np

@csrf_exempt
@require_http_methods(["GET", "POST"])
def investing_records_view(request, user_id):
    if request.method == 'GET':
        records = InvestingRecord.objects.filter(user_id=user_id)
        records_data = [
            {
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': float(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'amount_at_maturity': float(record.amount_at_maturity) if record.amount_at_maturity else None,
                'maturity_date': record.maturity_date.isoformat() if record.maturity_date else None,
                'cash_flows': json.loads(record.cash_flows) if record.cash_flows else None,
                'discount_rate': float(record.discount_rate) if record.discount_rate else None,
                'IRR': float(record.IRR) if record.IRR else None,
                'NPV': float(record.NPV) if record.NPV else None
            }
            for record in records
        ]
        return JsonResponse(records_data, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=user_id)
            record_date = datetime.strptime(data['record_date'], '%Y-%m-%d').date()
            tenor = int(data['tenor'])
            maturity_date = record_date + timedelta(days=tenor * 365)

            record = InvestingRecord.objects.create(
                user=user,
                title=data['title'],
                amount=data['amount'],
                record_date=record_date,
                tenor=tenor,
                type_invest=data['type_invest'],
                amount_at_maturity=data.get('amount_at_maturity', None),
                maturity_date=maturity_date,
                cash_flows=json.dumps(data.get('cash_flows', [])),
                discount_rate=data.get('discount_rate', None),
                IRR=data.get('IRR', None),
                NPV=data.get('NPV', None)
            )
            return JsonResponse({
                'id': record.id,
                'user_id': user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'amount_at_maturity': str(record.amount_at_maturity) if record.amount_at_maturity else None,
                'maturity_date': record.maturity_date.isoformat(),
                'cash_flows': json.loads(record.cash_flows) if record.cash_flows else None,
                'discount_rate': str(record.discount_rate) if record.discount_rate else None,
                'IRR': str(record.IRR) if record.IRR else None,
                'NPV': str(record.NPV) if record.NPV else None
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def investing_record_detail_view(request, user_id, record_id):
    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            record = get_object_or_404(InvestingRecord, id=record_id, user_id=user_id)

            # Update fields
            record.title = data.get('title', record.title)
            record.amount = data.get('amount', record.amount)
            record.tenor = data.get('tenor', record.tenor)
            record.type_invest = data.get('type_invest', record.type_invest)
            record.amount_at_maturity = data.get('amount_at_maturity', record.amount_at_maturity)
            record.cash_flows = json.dumps(data.get('cash_flows', json.loads(record.cash_flows)))
            record.discount_rate = data.get('discount_rate', record.discount_rate)

            

            record.save()
            return JsonResponse({
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'amount_at_maturity': str(record.amount_at_maturity) if record.amount_at_maturity else None,
                'maturity_date': record.maturity_date.isoformat() if record.maturity_date else None,
                'cash_flows': json.loads(record.cash_flows) if record.cash_flows else None,
                'discount_rate': str(record.discount_rate) if record.discount_rate else None,
                'IRR': str(record.IRR) if record.IRR else None,
                'NPV': str(record.NPV) if record.NPV else None
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            record = get_object_or_404(InvestingRecord, id=record_id, user_id=user_id)
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
