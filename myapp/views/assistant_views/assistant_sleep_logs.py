from django.http import JsonResponse
from myapp.models import SleepLog, User
from datetime import datetime
import json


def handle_sleep_log_action(action_data, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    action = action_data.get('action')
    
    if action == 'add_sleep_log':
        try:
            # Extract sleep log data from the request
            date = action_data.get('record_date')
            sleep_time = action_data.get('sleep_time')
            wake_time = action_data.get('wake_time')

            if not date or not sleep_time or not wake_time:
                return JsonResponse({"error": "Missing required fields: date, sleep_time, wake_time"}, status=400)

            # Parse date and time
            date_parsed = datetime.strptime(date, '%Y-%m-%d').date()
            sleep_time_parsed = datetime.strptime(sleep_time, '%Y-%m-%d %H:%M:%S')
            wake_time_parsed = datetime.strptime(wake_time, '%Y-%m-%d %H:%M:%S')

            # Create a new sleep log
            sleep_log = SleepLog.objects.create(
                user=user,
                date=date_parsed,
                sleep_time=sleep_time_parsed,
                wake_time=wake_time_parsed
            )
            return JsonResponse(sleep_log.to_dict(), status=200)

        except KeyError as e:
            return JsonResponse({"error": f"Missing field {str(e)}"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": f"Date/Time format error: {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid action for sleep log."}, status=400)
