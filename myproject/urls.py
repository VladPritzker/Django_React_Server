from django.urls import path
from myapp.views import users, financial_records, usersData
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('users/', users, name='users'),
    path('users/<int:user_id>/', usersData, name='user_details'),  # New endpoint to fetch user details by ID
    path('financial_records/', financial_records, name='get_financial_records'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
