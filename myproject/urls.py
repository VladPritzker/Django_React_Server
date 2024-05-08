from django.urls import path
from myapp.views import users, financial_records, usersData, investing_records,notes, note_detail_update, monthly_expenses
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('users/', users, name='users'),
    path('users/<int:user_id>/', usersData, name='user_details'),
    path('financial_records/', financial_records, name='get_financial_records'),
    path('investing_records/', investing_records, name='investing_records'),
    path('notes/', notes, name='notes'),
    path('notes/<int:user_id>/', notes, name='user_notes'),  # This line allows fetching specific notes
    path('notes/<int:user_id>/<int:note_id>/', note_detail_update, name='note_detail_update'),
    path('expenses/<int:user_id>/', monthly_expenses, name='monthly_expenses'),






    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
