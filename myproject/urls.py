from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import (
    user_views, income_views, meeting_views, financial_views,
    investing_views, note_views, expense_views, contact_views,
    sleep_logs, home_views, stock_data, customCashFlowInvestment_views,
    stock_data_pdf
)
from myapp.views.user_views import (
    register_user,  simple_login, 
    # register_user, login_with_otp, verify_otp, fetch_user_details, send_otp, simple_login, reset_password
)
from django.contrib.auth import views as auth_views

# docusign
from myapp.views.docusign_views.docusign_UI_send import send_docusign_envelope
# from myapp.views.docusign_views.endpoint_download_new_envelop import download_new_envelopes

# virtual assistant
from myapp.views.assistant_views import assistant_views

# plaid
from myapp.views.plaid.plaid_views import get_access_token, create_link_token, get_account_data, save_selected_accounts
from myapp.views.plaid.plaid_webhook import plaid_webhook
from myapp.views.plaid.nitifications import get_unread_notifications, mark_notifications_as_read

# password reset 
from myapp.views.password_reset.password_reset import reset_password_form, reset_password, request_password_reset

# authentification token 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from myapp.views.token import validate_token



from myapp.views.activities import ActivityTypesView, ActivitiesView










urlpatterns = [
    path('', home_views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
    path('simple-login/', simple_login, name='simple_login'),
    path('users/<int:user_id>/', user_views.users_data, name='users_data'),
    path('financial_records/', financial_views.financial_records, name='financial_records'),
    path('financial_records/<int:user_id>/<int:record_id>/', financial_views.delete_financial_record, name='delete_financial_record'),
    path('investing_records/<int:user_id>/', investing_views.investing_records_view, name='investing_records_list'),
    path('investing_records/<int:user_id>/<int:record_id>/', investing_views.investing_record_detail_view, name='investing_record_detail'),
    path('custom_cash_flow_investments/<int:user_id>/', customCashFlowInvestment_views.custom_cash_flow_investments, name='custom_cash_flow_investments'),
    path('custom_cash_flow_investments/<int:user_id>/<int:record_id>/', customCashFlowInvestment_views.custom_cash_flow_investment_detail, name='custom_cash_flow_investment_detail'),
    path('notes/', note_views.notes, name='notes'),
    path('notes/user/<int:user_id>/', note_views.notes, name='user_notes'),
    path('notes/user/<int:user_id>/<int:note_id>/', note_views.note_detail_update, name='note_detail_update'),
    path('notes/reorder/<int:user_id>/', note_views.reorder_notes, name='reorder_notes'),
    path('monthly_expenses/', expense_views.monthly_expenses, name='monthly_expenses'),
    path('monthly_expenses/<int:user_id>/', expense_views.monthly_expenses, name='user_monthly_expenses'),
    path('monthly_expenses/<int:user_id>/<int:expense_id>/', expense_views.expense_detail, name='expense_detail'),
    path('users/<int:user_id>/income_records/', income_views.income_records_view, name='income_records'),
    path('users/<int:user_id>/income_records/<int:record_id>/', income_views.income_record_detail_view, name='income_record_detail'),
    path('contacts/<int:user_id>/', contact_views.contact_list, name='contact_list'),
    path('contacts/<int:user_id>/<int:pk>/', contact_views.ContactDetailView.as_view(), name='contact_detail'),
    path('meetings/<int:user_id>/', meeting_views.meeting_list, name='meeting_list'),
    path('meetings/<int:user_id>/<int:pk>/', meeting_views.MeetingDetailView.as_view(), name='meeting_detail'),
    path('users/<int:user_id>/upload_photo/', user_views.upload_photo, name='upload_photo'),
    path('sleeplogs/<int:user_id>/', sleep_logs.SleepLogsView.as_view(), name='sleep_logs_list'),
    path('sleeplogs/<int:user_id>/<int:id>/', sleep_logs.SleepLogsView.as_view(), name='sleep_log_detail'),
    path('api/stock-data/', stock_data.stock_data_view, name='stock_data_view'),
    path('fetch-stock-data/', stock_data_pdf.fetch_stock_data, name='fetch_stock_data'),
    path('generate-pdf/', stock_data_pdf.generate_pdf, name='generate_pdf'),
    path('api/assistant/', assistant_views.assistant_views , name='assistant'),
    path('send-envelope/', send_docusign_envelope, name='send-envelope'),
    

    path('activity-types/<int:user_id>/', ActivityTypesView.as_view(), name='activity_types_list'),
    
    path('activity-types/<int:user_id>/<int:id>/', ActivityTypesView.as_view(), name='activity_types_detail'),

    path('activities/<int:user_id>/', ActivitiesView.as_view(), name='activities_list'),
    path('activities/<int:user_id>/<int:id>/', ActivitiesView.as_view(), name='activities_detail'),
 
    


    # plaid
    path('create_link_token/', create_link_token, name='create_link_token'),
    path('get_access_token/', get_access_token, name='get_access_token'),
    path('get_account_data/', get_account_data, name='get_account_data'),
    path('plaid/webhook/', plaid_webhook, name='plaid_webhook'),
    path('save_selected_accounts/', save_selected_accounts, name='save_selected_accounts'),
    
    # password reset 
    path('reset-password/', reset_password_form, name='reset_password_form'),  # GET request for form
    path('reset-password-submit/', reset_password, name='reset_password'),  # POST request for submission
    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    
    # authentification token 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/validate-token/', validate_token, name='validate_token'),


    # notifications
    path('notifications/', get_unread_notifications, name='get_unread_notifications'),
    path('notifications/mark_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

