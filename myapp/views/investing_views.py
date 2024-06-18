from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import InvestingRecord, User
import json
from datetime import datetime, timedelta
from decimal import Decimal




@csrf_exempt
def investing_records(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        records = InvestingRecord.objects.filter(user_id=user_id) if user_id else InvestingRecord.objects.all()
        records_data = [
            {
                'id': record.id, 'user_id': record.user.id,
                'title': record.title,
                'amount': float(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'amount_at_maturity': float(record.amount_at_maturity) if record.amount_at_maturity else None,
                'rate': float(record.rate) if record.rate else None,
                'maturity_date': record.maturity_date.isoformat() if record.maturity_date else None
            }
            for record in records
        ]
        return JsonResponse(records_data, safe=False)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=data['user_id'])
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
                rate=data.get('rate', None),
                maturity_date=maturity_date
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
                'rate': str(record.rate) if record.rate else None,
                'maturity_date': record.maturity_date.isoformat()
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            record_id = data.get('id')
            if not record_id:
                return JsonResponse({'error': 'Missing record ID'}, status=400)
            record = get_object_or_404(InvestingRecord, id=record_id)
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)