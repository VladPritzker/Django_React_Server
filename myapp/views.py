from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FinancialRecord, User
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
                    'money_invested': str(user.money_invested),  # Ensure these fields exist and are serialized correctly
                    'money_spent': str(user.money_spent),
                    'balance': str(user.balance),
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        else:
            return JsonResponse({'error': 'No valid action specified'}, status=400)
    
    elif request.method == 'GET':
        # Handle GET requests here, for example, to retrieve user information
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

            # Parse the record_date from string to date object
            parsed_date = datetime.strptime(record_date, '%Y-%m-%d').date()  # Ensure the date format matches your input

            user = User.objects.get(id=user_id)  # Retrieve the user instance

            # Create the financial record
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
                'amount': str(record.amount),  # Convert Decimal to string for JSON serialization
                'record_date': record.record_date.isoformat()  # Now calling isoformat on a date object
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as ve:
            return JsonResponse({'error': 'Date format error: ' + str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

    elif request.method == 'GET':
        user_id = request.GET.get('user_id')  # Optional filtering by user ID
        records = FinancialRecord.objects.all()

        if user_id:
            records = records.filter(user_id=user_id)

        records_data = [
            {
                'id': record.id,
                'user_id': record.user.id,
                'record_date': record.record_date.isoformat(),
                'title': record.title,
                'amount': float(record.amount)
            }
            for record in records
        ]
        return JsonResponse(records_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)