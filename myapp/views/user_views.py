from rest_framework_simplejwt.tokens import RefreshToken
import boto3
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.core.files.storage import default_storage  # For file storage (DigitalOcean Spaces)
from django.core.files.base import ContentFile  # For handling uploaded files
from decimal import Decimal, InvalidOperation  
import json
import traceback
import pyotp  # OTP library
from django.shortcuts import get_object_or_404
from django.conf import settings
from myapp.views.income_views import update_income_by_periods
from myapp.views.financial_views import update_spending_by_periods
from myapp.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import api_view, permission_classes






@csrf_exempt
def simple_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Authenticate user credentials
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in (Django session)
            login(request, user)

            # Generate JWT tokens (refresh and access tokens)
            refresh = RefreshToken.for_user(user)

            return JsonResponse({
                'message': 'Login successful',
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),  # Send the access token
                'refresh': str(refresh),  # Send the refresh token
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


User = get_user_model()
otp_storage = {}  # Store OTPs temporarily

### User Registration View
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'message': 'User registered successfully', 'id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@api_view(['PATCH', 'GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def users_data(request, user_id=None):
    if request.method == 'PATCH':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for updates'}, status=400)
        try:
            data = json.loads(request.body)
            user = User.objects.get(pk=user_id)

            for key, value in data.items():
                if hasattr(user, key):                     
                    # Attempt to convert to Decimal if possible
                    try:
                        if isinstance(getattr(user, key), Decimal):
                            setattr(user, key, Decimal(value))
                        else:
                            setattr(user, key, value)
                    except InvalidOperation:
                        return JsonResponse({'error': f'Invalid value for field {key}: {value}'}, status=400)
                else:
                    return JsonResponse({'error': f'Invalid field: {key}'}, status=400)
                user.save()
            # Refetch the user to get updated values
            user.refresh_from_db()

            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'money_invested': float(user.money_invested),
                'income_by_week': float(user.income_by_week),
                'income_by_month': float(user.income_by_month),
                'income_by_year': float(user.income_by_year),
                'spent_by_week': float(user.spent_by_week),
                'spent_by_month': float(user.spent_by_month),
                'spent_by_year': float(user.spent_by_year),
                'money_spent': float(user.money_spent),
                'balance': float(user.balance),
                'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'photo': user.photo
            }

            return JsonResponse({'message': 'User updated successfully', 'user': response_data}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            error_trace = traceback.format_exc()
            print(error_trace)  # Print the full error trace to the console or log it
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                update_income_by_periods(user)
                update_spending_by_periods(user)                

                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': float(user.money_invested),
                    'income_by_week': float(user.income_by_week),
                    'money_spent': float(user.money_spent),
                    'balance': float(user.balance),
                    'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                    'spent_by_week': float(user.spent_by_week) if user.spent_by_week else None,
                    'spent_by_month': float(user.spent_by_month) if user.spent_by_month else None,
                    'spent_by_year': float(user.spent_by_year) if user.spent_by_year else None,
                    'income_by_month': float(user.income_by_month) if user.income_by_month else None,
                    'income_by_year': float(user.income_by_year) if user.income_by_year else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'photo': user.photo  # Return the URL for the photo
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID is required'}, status=400)

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.create(**data)
            return JsonResponse({'message': 'User created successfully', 'id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for deletion'}, status=400)
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def upload_photo(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST' and request.FILES.get('photo'):
        try:
            photo = request.FILES['photo']
            file_name = f"user_{user.id}/{photo.name}"

            # Store the uploaded file using Django's default storage (DigitalOcean Spaces)
            saved_file = default_storage.save(file_name, ContentFile(photo.read()))

            # Get the URL of the uploaded file
            photo_url = default_storage.url(saved_file)

            # Update the user's photo field with the URL
            user.photo = photo_url
            user.save()

            return JsonResponse({'message': 'Photo uploaded successfully', 'photo_url': photo_url}, status=200)

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No photo uploaded'}, status=400)