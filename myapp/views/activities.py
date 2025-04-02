# views/activity_types_view.py
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


from myapp.models import Activity, ActivityType, User


@method_decorator(csrf_exempt, name='dispatch')
class ActivityTypesView(View):
    def get(self, request, user_id, id=None):
        """
        GET /activity-types/<user_id>/         -> List all activity types
        GET /activity-types/<user_id>/<id>/    -> Retrieve single type
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        if id:
            # detail
            try:
                activity_type = ActivityType.objects.get(id=id, user=user)
                return JsonResponse(activity_type.to_dict(), safe=False)
            except ActivityType.DoesNotExist:
                return JsonResponse({"error": "ActivityType not found"}, status=404)
        else:
            # list
            types = ActivityType.objects.filter(user=user)
            data = [t.to_dict() for t in types]
            return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})

    def post(self, request, user_id):
        """
        POST /activity-types/<user_id>/
        JSON body: { "name": "Reading" }
        Creates a new ActivityType for the user
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
            if "name" not in data:
                return JsonResponse({"error": "Missing 'name' field."}, status=400)

            activity_type = ActivityType(
                user=user,
                name=data["name"]
            )
            activity_type.save()
            return JsonResponse(activity_type.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def patch(self, request, user_id, id):
        """
        PATCH /activity-types/<user_id>/<id>/
        JSON body: { "name": "NewName" }
        Updates partial fields of the ActivityType
        """
        try:
            user = User.objects.get(id=user_id)
            activity_type = ActivityType.objects.get(id=id, user=user)
        except (User.DoesNotExist, ActivityType.DoesNotExist):
            return JsonResponse({"error": "User or ActivityType not found"}, status=404)

        try:
            data = json.loads(request.body)
            if "name" in data:
                activity_type.name = data["name"]
            activity_type.save()
            return JsonResponse(activity_type.to_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, user_id, id):
        """
        DELETE /activity-types/<user_id>/<id>/
        Deletes that ActivityType
        """
        try:
            user = User.objects.get(id=user_id)
            activity_type = ActivityType.objects.get(id=id, user=user)
        except (User.DoesNotExist, ActivityType.DoesNotExist):
            return JsonResponse({"error": "User or ActivityType not found"}, status=404)

        activity_type.delete()
        return JsonResponse({"message": "ActivityType deleted successfully"}, status=200)









@method_decorator(csrf_exempt, name='dispatch')
class ActivitiesView(View):
    def get(self, request, user_id, id=None):
        """
        GET /activities/<user_id>/
          - Optional query params:
              ?type_id=3 to filter by an ActivityType
              ?filter_date=YYYY-MM-DD to filter exact date
        GET /activities/<user_id>/<int:id>/
          - Retrieve a single activity by ID
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        if id:
            # Detail GET
            try:
                activity = Activity.objects.get(id=id, user=user)
                return JsonResponse(activity.to_dict(), safe=False)
            except Activity.DoesNotExist:
                return JsonResponse({"error": "Activity not found"}, status=404)
        else:
            # List GET
            type_id = request.GET.get("type_id")
            filter_date = request.GET.get("filter_date")

            activities = Activity.objects.filter(user=user)

            # Filter by type if provided (and not 'all')
            if type_id and type_id.lower() != "all":
                activities = activities.filter(activity_type_id=type_id)

            # Filter by exact date if provided
            if filter_date:
                activities = activities.filter(date=filter_date)

            data = [a.to_dict() for a in activities]
            return JsonResponse(data, safe=False, json_dumps_params={'indent': 2})

    def post(self, request, user_id):
        """
        POST /activities/<user_id>/
        JSON: { "activity_type_id": 3, "date": "2025-01-01" }
        Creates a new Activity referencing an existing ActivityType
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            data = json.loads(request.body)
            if 'activity_type_id' not in data or 'date' not in data:
                return JsonResponse({"error": "Missing 'activity_type_id' or 'date'."}, status=400)

            # Check that the ActivityType belongs to this user
            try:
                activity_type = ActivityType.objects.get(id=data['activity_type_id'], user=user)
            except ActivityType.DoesNotExist:
                return JsonResponse({"error": "ActivityType not found or doesn't belong to this user"}, status=404)

            activity = Activity(user=user, activity_type=activity_type, date=data['date'])
            activity.save()
            return JsonResponse(activity.to_dict(), status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def patch(self, request, user_id, id):
        """
        PATCH /activities/<user_id>/<int:id>/
        Example JSON: { "activity_type_id": 2, "date": "2025-01-01" }
        """
        try:
            user = User.objects.get(id=user_id)
            activity = Activity.objects.get(id=id, user=user)
        except (User.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({"error": "User or Activity not found"}, status=404)

        try:
            data = json.loads(request.body)

            if "activity_type_id" in data:
                # Validate new activity type
                try:
                    new_type = ActivityType.objects.get(id=data['activity_type_id'], user=user)
                    activity.activity_type = new_type
                except ActivityType.DoesNotExist:
                    return JsonResponse({"error": "New ActivityType not found or not user's"}, status=404)

            if "date" in data:
                activity.date = data["date"]

            activity.save()
            return JsonResponse(activity.to_dict())
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def delete(self, request, user_id, id):
        """
        DELETE /activities/<user_id>/<int:id>/
        """
        try:
            user = User.objects.get(id=user_id)
            activity = Activity.objects.get(id=id, user=user)
        except (User.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({"error": "User or Activity not found"}, status=404)

        activity.delete()
        return JsonResponse({"message": "Activity deleted successfully"}, status=200)