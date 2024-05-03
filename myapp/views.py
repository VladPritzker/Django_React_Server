from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FinancialRecord, User, InvestingRecord
from datetime import datetime




@csrf_exempt
def users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'register':
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'message': 'User registered successfully', 'id': user.id}, status=201)

        elif action == 'login':
            user = authenticate(email=data.get('email'), password=data.get('password'))
            if user is not None:
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': str(user.money_invested),
                    'money_spent': str(user.money_spent),
                    'balance': str(user.balance),
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        elif action == 'fetch_user_details':
            user_id = data.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': str(user.money_invested),
                    'money_spent': str(user.money_spent),
                    'balance': str(user.balance),
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

    elif request.method == 'GET':
        users = User.objects.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(users_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def usersData(request, user_id=None):
    if request.method == 'GET':
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': float(user.money_invested),
                    'money_spent': float(user.money_spent),
                    'balance': float(user.balance),
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            users = User.objects.all()
            users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return JsonResponse(users_data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def financial_records(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            title = data.get('title')
            amount = data.get('amount')
            record_date = data.get('record_date')

            parsed_date = datetime.strptime(record_date, '%Y-%m-%d').date()
            user = User.objects.get(id=user_id)

            record = FinancialRecord.objects.create(
                user=user,
                title=title,
                amount=amount,
                record_date=parsed_date
            )
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
def investing_records(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ['user_id', 'title', 'amount', 'record_date', 'tenor', 'type_invest']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': 'Missing required fields: ' + ', '.join(missing_fields)}, status=400)

        try:
            user_id = data['user_id']
            user = User.objects.get(id=user_id)  # Ensure user exists

            record = InvestingRecord.objects.create(
                user=user,
                title=data['title'],
                amount=data['amount'],
                record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
                tenor=data['tenor'],
                type_invest=data['type_invest']
            )
            return JsonResponse({
                'id': record.id,
                'user_id': user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': data['type_invest']
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as ve:
            return JsonResponse({'error': 'Data format error: ' + str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        records = InvestingRecord.objects.filter(user_id=user_id) if user_id else InvestingRecord.objects.all()
        records_data = [
            {'id': record.id, 'user_id': record.user.id, 'title': record.title, 'amount': float(record.amount),
             'record_date': record.record_date.isoformat(), 'tenor': record.tenor, 'type_invest': record.type_invest}
            for record in records
        ]
        return JsonResponse(records_data, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
