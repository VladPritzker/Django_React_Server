# views.py

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from myapp.models import CustomCashFlowInvestment, User
import json
from datetime import datetime
import numpy as np

@csrf_exempt
@require_http_methods(["GET", "POST"])
def custom_cash_flow_investments(request, user_id):
    if request.method == 'GET':
        records = CustomCashFlowInvestment.objects.filter(user_id=user_id)
        records_data = [
            {
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': float(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'cash_flows': json.loads(record.cash_flows),
                'discount_rate': float(record.discount_rate),
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
            record = CustomCashFlowInvestment.objects.create(
                user=user,
                title=data['title'],
                amount=data['amount'],
                record_date=record_date,
                tenor=data['tenor'],
                type_invest=data['type_invest'],
                cash_flows=json.dumps(data['cash_flows']),
                discount_rate=data['discount_rate'],
                IRR=data.get('IRR'),
                NPV=data.get('NPV')
            )
            return JsonResponse({
                'id': record.id,
                'user_id': user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'cash_flows': json.loads(record.cash_flows),
                'discount_rate': str(record.discount_rate),
                'IRR': str(record.IRR) if record.IRR else None,
                'NPV': str(record.NPV) if record.NPV else None
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PATCH", "DELETE"])
def custom_cash_flow_investment_detail(request, user_id, record_id):
    record = get_object_or_404(CustomCashFlowInvestment, id=record_id, user_id=user_id)

    if request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            record.title = data.get('title', record.title)
            record.amount = data.get('amount', record.amount)
            record.tenor = data.get('tenor', record.tenor)
            record.type_invest = data.get('type_invest', record.type_invest)
            record.cash_flows = json.dumps(data.get('cash_flows', json.loads(record.cash_flows)))
            record.discount_rate = data.get('discount_rate', record.discount_rate)
            record.IRR = data.get('IRR', record.IRR)
            record.NPV = data.get('NPV', record.NPV)
            record.save()
            return JsonResponse({
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'cash_flows': json.loads(record.cash_flows),
                'discount_rate': str(record.discount_rate),
                'IRR': str(record.IRR) if record.IRR else None,
                'NPV': str(record.NPV) if record.NPV else None
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

