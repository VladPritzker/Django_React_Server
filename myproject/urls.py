from django.urls import path
from django.contrib.auth import views as auth_views
from myapp.views import (
    users, financial_records, usersData, investing_records, notes, note_detail_update,
    monthly_expenses, expense_detail, reorder_notes, upload_photo, delete_financial_record,
    income_records_view, income_record_detail_view, contact_list, ContactDetailView,
    meeting_list, MeetingDetailView, add_income_record, delete_income_record
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', users, name='users'),
    path('users/<int:user_id>/', usersData, name='user_details'),
    path('investing_records/', investing_records, name='investing_records'),
    path('notes/', notes, name='notes'),
    path('notes/<int:user_id>/', notes, name='user_notes'),  # This line allows fetching specific notes
    path('notes/<int:user_id>/<int:note_id>/', note_detail_update, name='note_detail_update'),
    path('expenses/<int:user_id>/', monthly_expenses, name='monthly_expenses'),
    path('expenses/', monthly_expenses, name='monthly_expenses'),
    path('expenses/<int:user_id>/<int:expense_id>/', expense_detail, name='monthly_expenses'),
    path('notes/<int:user_id>/reorder/', reorder_notes, name='reorder_notes'),  # New path for reordering notes
    path('users/<int:user_id>/upload_photo/', upload_photo, name='upload_photo'),
    path('financial_records/<int:user_id>/<int:record_id>/', delete_financial_record, name='delete_financial_record'),
    path('financial_records/', financial_records, name='get_financial_records'),
    path('users/<int:user_id>/contacts/', contact_list, name='contact-list'),
    path('users/<int:user_id>/contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),
    path('users/<int:user_id>/income_records/', income_records_view, name='income-records-view'),
    path('users/<int:user_id>/income_records/add/', add_income_record, name='add_income_record'),
    path('users/<int:user_id>/income_records/<int:record_id>/', income_record_detail_view, name='income-record-detail-view'),
    path('users/<int:user_id>/income_records/<int:record_id>/delete/', delete_income_record, name='delete_income_record'),
    path('users/<int:user_id>/meetings/', meeting_list, name='meeting-list'),
    path('users/<int:user_id>/meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),

    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
