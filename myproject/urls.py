from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views.user_views import users, users_data, upload_photo, csrf_token_view  # Import the view
from myapp.views.income_views import income_records_view, income_record_detail_view, add_income_record, delete_income_record
from myapp.views.meeting_views import meeting_list, MeetingDetailView
from myapp.views.financial_views import financial_records, delete_financial_record
from myapp.views.investing_views import investing_records_view, investing_record_detail_view
from myapp.views.note_views import notes, note_detail_update, reorder_notes
from myapp.views.expense_views import monthly_expenses, expense_detail
from myapp.views.contact_views import contact_list, ContactDetailView
from myapp.views import sleep_logs
from myapp.views.home_views import homepage
from myapp.views.stock_data import stock_data_view



urlpatterns = [
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('users/', users, name='users'),
    path('users/<int:user_id>/', users_data, name='users_data'),
    path('financial_records/', financial_records, name='financial_records'),
    path('financial_records/<int:user_id>/<int:record_id>/', delete_financial_record, name='delete_financial_record'),
    path('investing_records/<int:user_id>/', investing_records_view, name='investing_records_list'),
    path('investing_records/<int:user_id>/<int:record_id>/', investing_record_detail_view, name='investing_record_detail'),
    path('notes/', notes, name='notes'),
    path('notes/user/<int:user_id>/', notes, name='user_notes'),
    path('notes/user/<int:user_id>/<int:note_id>/', note_detail_update, name='note_detail_update'),
    path('notes/reorder/<int:user_id>/', reorder_notes, name='reorder_notes'),
    path('monthly_expenses/', monthly_expenses, name='monthly_expenses'),
    path('monthly_expenses/<int:user_id>/', monthly_expenses, name='user_monthly_expenses'),
    path('monthly_expenses/<int:user_id>/<int:expense_id>/', expense_detail, name='expense_detail'),
    path('users/<int:user_id>/income_records/', income_records_view, name='income_records'),
    path('users/<int:user_id>/income_records/<int:record_id>/', income_record_detail_view, name='income_record_detail'),
    path('users/<int:user_id>/add_income/', add_income_record, name='add_income_record'),
    path('users/<int:user_id>/delete_income/<int:record_id>/', delete_income_record, name='delete_income_record'),
    path('contacts/<int:user_id>/', contact_list, name='contact_list'),
    path('contacts/<int:user_id>/<int:pk>/', ContactDetailView.as_view(), name='contact_detail'),
    path('meetings/<int:user_id>/', meeting_list, name='meeting_list'),
    path('meetings/<int:user_id>/<int:pk>/', MeetingDetailView.as_view(), name='meeting_detail'),
    path('users/<int:user_id>/upload_photo/', upload_photo, name='upload_photo'),  # Add this line
    path('sleeplogs/<int:user_id>/', sleep_logs.SleepLogsView.as_view(), name='sleep_logs_list'),
    path('sleeplogs/<int:user_id>/<int:id>/', sleep_logs.SleepLogsView.as_view(), name='sleep_log_detail'),
    path('get_csrf_token/', csrf_token_view, name='get_csrf_token'),  # Add this line
    path('api/stock-data/', stock_data_view, name='stock_data_view'),
    







    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)