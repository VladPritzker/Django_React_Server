from django.contrib.auth import authenticate
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

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
                    'money_invested': user.money_invested,
                    'money_spent': user.money_spent,
                    'balance': user.balance
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
