import json
import logging
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import User

# Set up logging
logger = logging.getLogger(__name__)

@csrf_exempt
def users(request):
    if request.method == 'GET':
        try:
            users = User.objects.all()
            data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return JsonResponse(data, safe=False)
        except Exception as e:
            logger.error("Error getting users: %s", e)
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User(
                username=data['username'],
                email=data['email'],
                password=make_password(data['password'])
            )
            user.save()
            return JsonResponse({'message': 'User registered successfully'}, status=201)
        except Exception as e:
            logger.error("Failed to register user: %s", e)
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
