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





@csrf_exempt
def simple_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            return JsonResponse({
                'message': 'Login successful',
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=200)
        else:
            # If authentication fails
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



### OTP-Based Login View
@csrf_exempt
def login_with_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(email=data.get('email'), password=data.get('password'))
        if user is not None:
            otp = pyotp.random_base32()
            otp_code = pyotp.TOTP(otp).now()

            # Store OTP with expiration
            otp_storage[user.email] = {
                'otp': otp_code,
                'expires_at': timezone.now() + timedelta(minutes=5)
            }

            # Send OTP via email
            try:
                send_mail(
                    'Your Login OTP',
                    f'Welcome to Pritzker Finance. Your OTP code is: {otp_code}',
                    'no-reply@yourdomain.com',
                    [user.email],
                    fail_silently=False
                )
                return JsonResponse({
                    'message': 'OTP sent to your email. Please verify.',
                    'id': user.id,
                }, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Failed to send OTP'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Log the received email and password for debugging
        print(f"Email: {email}, Password: {password}")

        user = authenticate(email=email, password=password)  # Check if this returns a user

        if user is not None:
            otp = pyotp.random_base32()
            otp_code = pyotp.TOTP(otp).now()

            # Store OTP with expiration
            otp_storage[user.email] = {
                'otp': otp_code,
                'expires_at': timezone.now() + timedelta(minutes=5)
            }

            # Send OTP via email
            try:
                send_mail(
                    'Your Login OTP',
                    f'Welcome to Pritzker Finance. Your OTP code is: {otp_code}',
                    'no-reply@yourdomain.com',
                    [user.email],
                    fail_silently=False
                )
                return JsonResponse({'message': 'OTP sent to your email. Please verify.', 'id': user.id}, status=200)
            except Exception as e:
                return JsonResponse({'error': 'Failed to send OTP'}, status=500)
        else:
            print("Invalid credentials")  # Log for debugging
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



### OTP Verification View
@csrf_exempt
def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')

        # Verify the OTP
        stored_otp = otp_storage.get(email)
        if not stored_otp:
            return JsonResponse({'error': 'OTP expired or invalid'}, status=400)

        if stored_otp['otp'] == otp and timezone.now() <= stored_otp['expires_at']:
            user = User.objects.get(email=email)
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
                'is_superuser': user.is_superuser
            }, status=200)
        else:
            return JsonResponse({'error': 'OTP is incorrect or expired'}, status=401)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


### Password Reset View
@csrf_exempt
def reset_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            user = get_object_or_404(User, email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"

            # Send password reset email
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'reset_link': reset_link,
            })
            send_mail(
                'Password Reset Request',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                html_message=message,
            )
            return JsonResponse({'message': 'Password reset link sent.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            return JsonResponse({'error': 'Failed to send password reset email.'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


### Fetch User Details View
@csrf_exempt
def fetch_user_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
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
                'photo': default_storage.url(user.photo) if user.photo else None  # Return the photo URL
            })
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)







@csrf_exempt
def users_data(request, user_id=None):
    if request.method == 'PATCH':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for updates'}, status=400)
        try:
            data = json.loads(request.body)
            user = User.objects.get(pk=user_id)

            for key, value in data.items():
                if hasattr(user, key):
                    print(f"Updating {key} to {value}")  # Logging the field being updated
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