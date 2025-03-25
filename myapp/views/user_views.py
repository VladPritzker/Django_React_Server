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

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'message': 'Login successful',
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

User = get_user_model()
otp_storage = {}  # Store OTPs temporarily

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

            # Update fields
            for key, value in data.items():
                if hasattr(user, key):
                    try:
                        current_val = getattr(user, key)
                        # If the field is a Decimal in the model, attempt to set it to Decimal
                        if isinstance(current_val, Decimal):
                            setattr(user, key, Decimal(value))
                        else:
                            setattr(user, key, value)
                    except InvalidOperation:
                        return JsonResponse({'error': f'Invalid value for field {key}: {value}'}, status=400)
                else:
                    return JsonResponse({'error': f'Invalid field: {key}'}, status=400)

            user.save()
            user.refresh_from_db()

            # Convert any possible None decimals to None in JSON, else float
            response_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'money_invested': float(user.money_invested) if user.money_invested is not None else None,
                'income_by_week': float(user.income_by_week) if user.income_by_week is not None else None,
                'income_by_month': float(user.income_by_month) if user.income_by_month is not None else None,
                'income_by_year': float(user.income_by_year) if user.income_by_year is not None else None,
                'spent_by_week': float(user.spent_by_week) if user.spent_by_week is not None else None,
                'spent_by_month': float(user.spent_by_month) if user.spent_by_month is not None else None,
                'spent_by_year': float(user.spent_by_year) if user.spent_by_year is not None else None,
                'money_spent': float(user.money_spent) if user.money_spent is not None else None,
                'balance': float(user.balance) if user.balance is not None else None,
                'balance_goal': float(user.balance_goal) if user.balance_goal is not None else None,
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
            print(error_trace)
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
                    'money_invested': float(user.money_invested) if user.money_invested is not None else None,
                    'income_by_week': float(user.income_by_week) if user.income_by_week is not None else None,
                    'money_spent': float(user.money_spent) if user.money_spent is not None else None,
                    'balance': float(user.balance) if user.balance is not None else None,
                    'balance_goal': float(user.balance_goal) if user.balance_goal is not None else None,
                    'spent_by_week': float(user.spent_by_week) if user.spent_by_week is not None else None,
                    'spent_by_month': float(user.spent_by_month) if user.spent_by_month is not None else None,
                    'spent_by_year': float(user.spent_by_year) if user.spent_by_year is not None else None,
                    'income_by_month': float(user.income_by_month) if user.income_by_month is not None else None,
                    'income_by_year': float(user.income_by_year) if user.income_by_year is not None else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'photo': user.photo
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
            saved_file = default_storage.save(file_name, ContentFile(photo.read()))
            photo_url = default_storage.url(saved_file)

            user.photo = photo_url
            user.save()
            return JsonResponse({'message': 'Photo uploaded successfully', 'photo_url': photo_url}, status=200)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'No photo uploaded'}, status=400)