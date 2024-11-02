from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from myapp.models import User  # Assuming you have a User model
from django.contrib.auth.hashers import make_password
import uuid
from datetime import timedelta
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def request_password_reset(request):
    email = request.POST.get('email')
    user = User.objects.filter(email=email).first()
    
    if user:
        token = uuid.uuid4().hex
        user.reset_token = token
        user.reset_token_expiry = timezone.now() + timedelta(hours=1)
        user.save()

        reset_link = f"{settings.BASE_URL}/reset-password?token={token}"
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=email,
            subject="Password Reset Request",
            html_content=f"<p>Hello {user.username},</p><p><a href='{reset_link}'>Reset Password</a></p>"
        )

        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            logger.info(f"Email sent with status code: {response.status_code}")
        except Exception as e:
            logger.error(f"SendGrid Error: {e}")
            
    return JsonResponse({"message": "If an account exists for this email, a reset link has been sent."})




@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        token = request.POST.get('token')
        new_password = request.POST.get('password')
        logger.info(f"SENDGRID_API_KEY: {settings.SENDGRID_API_KEY}")

        user = User.objects.filter(reset_token=token).first()
        
        if user:
            # Check if reset_token_expiry is set and not expired
            if user.reset_token_expiry and user.reset_token_expiry > timezone.now():
                user.password = make_password(new_password)
                user.reset_token = None  # Clear the token
                user.reset_token_expiry = None
                user.save()
                return JsonResponse({"message": "Password reset successful."})
            else:
                return JsonResponse({"message": "Invalid or expired token."})
        else:
            return JsonResponse({"message": "User not found."})
        

# Sendgrid        
api_key = os.getenv("SENDGRID_API_KEY")
message = Mail(
    from_email='pritzkervlad@gmail.com',
    to_emails='pritzkervlad@gmail.com',
    subject='Hello from SendGrid!',
    html_content='<strong>This is a test email from SendGrid API</strong>'
)

try:
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    response = sg.send(message)
    logger.info(f"Email status code: {response.status_code}")
except Exception as e:
    logger.error(f"SendGrid Exception: {str(e)}")

