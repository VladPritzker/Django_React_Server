from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid
from datetime import timedelta
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from myapp.models import User
from django.contrib.auth.hashers import make_password
import logging

logger = logging.getLogger(__name__)

# View to render the reset password form (GET request)
@csrf_exempt
def reset_password_form(request):
    try:
        token = request.GET.get('token')
        if not token:
            logger.error("No token provided in request.")
            return JsonResponse({"message": "Token is required."}, status=400)

        user = User.objects.filter(reset_token=token).first()
        if user and user.reset_token_expiry and user.reset_token_expiry > timezone.now():
            logger.info("Rendering reset password form.")
            return render(request, 'reset_password_form.html', {'token': token})
        else:
            logger.warning("Invalid or expired token.")
            return JsonResponse({"message": "Invalid or expired token."}, status=400)
    
    except Exception as e:
        logger.error(f"Error in reset_password_form view: {e}")
        return JsonResponse({"message": "Internal server error"}, status=500)

# View to handle the password reset submission (POST request)
@csrf_exempt
def reset_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('token')
            new_password = data.get('password')

            user = User.objects.filter(reset_token=token).first()
            if user and user.reset_token_expiry and user.reset_token_expiry > timezone.now():
                # Update password and clear token
                user.password = make_password(new_password)
                user.reset_token = None
                user.reset_token_expiry = None
                user.save()
                return JsonResponse({"message": "Password reset successful."})
            else:
                return JsonResponse({"message": "Invalid or expired token."}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
def request_password_reset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            logger.info(f"Received email for password reset: {email}")
            
            if not email:
                return JsonResponse({"message": "Email is required."}, status=400)

            user = User.objects.filter(email=email).first()
            if user:
                token = uuid.uuid4().hex
                user.reset_token = token
                user.reset_token_expiry = timezone.now() + timedelta(hours=1)
                user.save()

                reset_link = f"{settings.BASE_URL}/reset-password/?token={token}"
                subject = "Password Reset Request"
                message_content = f"""
                                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
                                    <h2 style="color: #004080; text-align: center;">Pritzker Finance</h2>
                                    <p>Hello {user.username},</p>
                                    <p>We received a request to reset your password for your Pritzker Finance account. If you made this request, please click the button below to reset your password:</p>
                                    <div style="text-align: center; margin: 20px 0;">
                                        <a href="{reset_link}" style="background-color: #0074b7; color: white; padding: 10px 20px; text-decoration: none; font-weight: bold; border-radius: 5px;">Reset Password</a>
                                    </div>
                                    <p>If you did not request a password reset, please ignore this email or contact our support team if you have any concerns.</p>
                                    <hr style="border: none; border-top: 1px solid #e0e0e0;">
                                    <p style="font-size: 0.9em; color: #666;">Thank you,<br>The Pritzker Finance Team</p>
                                    <p style="font-size: 0.8em; color: #999; text-align: center;">Pritzker Finance, 123 Financial Avenue, New York, NY 10001</p>
                                </div>
                                """


                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=email,
                    subject=subject,
                    html_content=message_content
                )

                try:
                    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                    response = sg.send(message)
                    logger.info(f"Password reset email sent successfully with status code: {response.status_code}")
                except Exception as e:
                    logger.error(f"Error sending password reset email: {e}")
                    return JsonResponse({"message": "Failed to send reset email."}, status=500)
            
            return JsonResponse({"message": "If an account exists for this email, a reset link has been sent."})
        except json.JSONDecodeError:
            logger.error("Invalid JSON format received")
            return JsonResponse({"message": "Invalid JSON format"}, status=400)
    return JsonResponse({"message": "Method not allowed"}, status=405)