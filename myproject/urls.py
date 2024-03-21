from django.urls import path
from myapp.views import DailyActivityListView

urlpatterns = [
    path('', DailyActivityListView.as_view(), name='daily-activity-list'),
]

