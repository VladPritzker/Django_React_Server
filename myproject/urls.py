from django.urls import path
from myapp.views import get_monthly_activities

urlpatterns = [
    path('activities/<int:year>/<int:month>/', get_monthly_activities, name='monthly-activities'),
]
