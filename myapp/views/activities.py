from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from decimal import Decimal, InvalidOperation
import json

from myapp.models import Activity, User

@method_decorator(csrf_exempt, name='dispatch')
class ActivitiesView(View):
    def get(self, request, user_id, id=None):
        """
        GET /activities/<user_id>/        -> List all activities for that user
        GET /activities/<user_id>/<int:id>/ -> Retrieve a single activity
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        if id:  # Detail GET
            try:
                activity = Activity.objects.get(id=id, user=user)
                return JsonResponse(activity.to_dict(), safe=False)
            except Activity.DoesNotExist:
                return JsonResponse({"error": "Activity not found"}, status=404)
        else:  # List GET
            activities = Activity.objects.filter(user=user)
            data = [a.to_dict() for a in activities]
            return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})

    def post(self, request, user_id):
        """
        POST /activities/<user_id>/
        Creates a new activity record for this user.
        Expected JSON: {"name": "...", "date": "YYYY-MM-DD"}
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
            # Basic validation
            if 'name' not in data or 'date' not in data:
                return JsonResponse({"error": "Missing 'name' or 'date' field."}, status=400)

            activity = Activity(
                user=user,
                name=data['name'],
                date=data['date']
            )
            activity.save()
            return JsonResponse(activity.to_dict(), status=201)
        except KeyError as e:
            return JsonResponse({"error": f"Missing field {str(e)}"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def patch(self, request, user_id, id):
        """
        PATCH /activities/<user_id>/<int:id>/
        Partially update an existing Activity.
        e.g., {"name": "New Name", "date": "2025-01-01"}
        """
        try:
            user = User.objects.get(id=user_id)
            activity = Activity.objects.get(id=id, user=user)
        except (User.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({"error": "User or Activity not found"}, status=404)

        try:
            data = json.loads(request.body)
            activity.name = data.get('name', activity.name)
            activity.date = data.get('date', activity.date)
            activity.save()
            return JsonResponse(activity.to_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, user_id, id):
        """
        DELETE /activities/<user_id>/<int:id>/
        Deletes the specified Activity record.
        """
        try:
            user = User.objects.get(id=user_id)
            activity = Activity.objects.get(id=id, user=user)
        except (User.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({"error": "User or Activity not found"}, status=404)

        activity.delete()
        return JsonResponse({"message": "Activity deleted successfully"}, status=200)
