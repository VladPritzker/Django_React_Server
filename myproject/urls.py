from django.urls import path
from myapp.views import users  # make sure to import the combined function
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('users/', users, name='users'),  # Updated to use the combined 'users' function
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]