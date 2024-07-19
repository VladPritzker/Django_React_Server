from django.core.mail import send_mail
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from decimal import Decimal
import json
import traceback
from django.template import TemplateDoesNotExist
from django.conf import settings
import os


from myapp.views.income_views import update_income_by_periods
from myapp.views.financial_views import update_spending_by_periods

User = get_user_model()

@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({'csrftoken': request.COOKIES['csrftoken']})

@csrf_exempt
def users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'register':
            try:
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )
                print(f"User created: {user}")  # Debugging line
                return JsonResponse({'message': 'User registered successfully', 'id': user.id}, status=201)
            except Exception as e:
                print(f"Error creating user: {e}")  # Debugging line
                return JsonResponse({'error': str(e)}, status=400)

        elif action == 'login':
            user = authenticate(email=data.get('email'), password=data.get('password'))
            if user is not None:
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
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
        

        
        elif action == 'reset_password':
            email = data.get('email')
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
                
                try:
                    # Attempt to load the template
                    template = get_template('reset_password_email.html')
                    print(f"Template found at: {template.origin}")
                except TemplateDoesNotExist:
                    print("Template reset_password_email.html does not exist.")
                    print(f"Template directories: {settings.TEMPLATES[0]['DIRS']}")
                    for directory in settings.TEMPLATES[0]['DIRS']:
                        if os.path.exists(directory):
                            print(f"Contents of {directory}: {os.listdir(directory)}")
                        else:
                            print(f"Directory does not exist: {directory}")
                    return JsonResponse({'error': 'Email template not found.'}, status=500)

                # Render the email content
                message = render_to_string('reset_password_email.html', {
                    'user': user,
                    'reset_link': reset_link,
                })
                send_mail(
                    'Password Reset Request',
                    message,
                    'no-reply@yourdomain.com',
                    [user.email],
                    fail_silently=False,
                    html_message=message,  # This is where the HTML content is passed

                )
                return JsonResponse({'message': 'Password reset link sent to your email.'}, status=200)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User with this email does not exist.'}, status=404)
            except Exception as e:
                print(f"SMTP error: {e}")
                return JsonResponse({'error': 'Failed to send email.'}, status=500)
        
        elif action == 'fetch_user_details':
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
                    'photo': user.photo.url if user.photo else None  # Convert ImageField to URL
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

    elif request.method == 'GET':
        users = User.objects.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(users_data, safe=False)

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
                'photo': user.photo.url if user.photo else None
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
                    'photo': user.photo.url if user.photo else None  # Convert ImageField to URL
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
            return JsonResponse({'message': 'User deleted successfully'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def upload_photo(request, user_id):
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            photo = request.FILES.get('photo')

            if not photo:
                return JsonResponse({'error': 'No photo uploaded'}, status=400)

            # Save the photo to the user's directory
            file_path = default_storage.save(f'user_{user_id}/{photo.name}', ContentFile(photo.read()))

            # Assuming you want to save the photo path to the user's profile
            user.photo = file_path
            user.save()

            return JsonResponse({'message': 'Photo uploaded successfully', 'file_url': file_path}, status=201)
        except Exception as e:
            # Log the error for debugging purposes
            error_trace = traceback.format_exc()
            print(error_trace)  # Print the error trace to the console or use logging
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
