from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from myapp.views import (
    user_views, income_views, meeting_views, financial_views,
    investing_views, note_views, expense_views, contact_views,
    sleep_logs, home_views, stock_data, customCashFlowInvestment_views,
    stock_data_pdf, docusign_views
)
import myapp.views as download_pdf

urlpatterns = [
    path('', home_views.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('users/', user_views.users, name='users'),
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
    path('get_csrf_token/', user_views.csrf_token_view, name='get_csrf_token'),
    path('api/stock-data/', stock_data.stock_data_view, name='stock_data_view'),
    path('fetch-stock-data/', stock_data_pdf.fetch_stock_data, name='fetch_stock_data'),
    path('generate-pdf/', stock_data_pdf.generate_pdf, name='generate_pdf'),

     # DocuSign Endpoints
    path('docusign/webhook/', docusign_views.docusign_webhook, name='docusign_webhook'),
    path('download-envelope-pdf/', docusign_views.download_envelope_pdf, name='download-envelope-pdf'),
    path('download_pdf/<str:envelope_id>/', download_pdf, name='download_pdf'),



     

    
    


    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
