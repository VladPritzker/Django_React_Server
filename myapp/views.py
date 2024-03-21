from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DailyActivity

class DailyActivityListView(APIView):
    def get(self, request):
        activities = DailyActivity.objects.order_by('date')  
        data = [{'date': activity.date,
                 'slept': activity.slept,
                 'studied': activity.studied,
                 'wokeUp': activity.wokeUp} for activity in activities]
        return Response(data)
    
