# views/sleep_logs.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from myapp.models import SleepLog, User
import json

@method_decorator(csrf_exempt, name='dispatch')
class SleepLogsView(View):
    def get(self, request, user_id, id=None):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
 
        if id:
            try:
                sleep_log = SleepLog.objects.get(id=id, user=user)
                return JsonResponse(sleep_log.to_dict(), safe=False)
            except SleepLog.DoesNotExist:
                return JsonResponse({"error": "SleepLog not found"}, status=404)
        else:
            sleep_logs = SleepLog.objects.filter(user=user)
            return JsonResponse([log.to_dict() for log in sleep_logs], safe=False, json_dumps_params={'indent': 2})

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
            sleep_log = SleepLog(
                user=user, 
                date=data['date'], 
                sleep_time=data['sleep_time'], 
                wake_time=data['wake_time']
            )
            sleep_log.save()
            return JsonResponse(sleep_log.to_dict(), status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def put(self, request, user_id, id):
        try:
            user = User.objects.get(id=user_id)
            sleep_log = SleepLog.objects.get(id=id, user=user)
        except (User.DoesNotExist, SleepLog.DoesNotExist):
            return JsonResponse({"error": "User or SleepLog not found"}, status=404)

        try:
            data = json.loads(request.body)
            sleep_log.date = data.get('date', sleep_log.date)
            sleep_log.sleep_time = data.get('sleep_time', sleep_log.sleep_time)
            sleep_log.wake_time = data.get('wake_time', sleep_log.wake_time)
            sleep_log.save()
            return JsonResponse(sleep_log.to_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, user_id, id):
        try:
            user = User.objects.get(id=user_id)
            sleep_log = SleepLog.objects.get(id=id, user=user)
        except (User.DoesNotExist, SleepLog.DoesNotExist):
            return JsonResponse({"error": "User or SleepLog not found"}, status=404)

        sleep_log.delete()
        return JsonResponse({"message": "SleepLog deleted successfully"}, status=204)
