from django.http import JsonResponse
from .models import get_daily_activity_model

def get_monthly_activities(request, year, month):
    DailyActivity = get_daily_activity_model(year, month)
    try:
        activities = DailyActivity.objects.all().order_by('date')
        data = [{
            'date': activity.date.isoformat(),
            'slept': str(activity.slept) if activity.slept else None,
            'studied': activity.studied,
            'wokeUp': str(activity.wokeUp) if activity.wokeUp else None
        } for activity in activities]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
