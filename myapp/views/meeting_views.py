from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import datetime
from myapp.models import Meeting, User
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class MeetingDetailView(View):

    def get(self, request, user_id, pk):
        meeting = get_object_or_404(Meeting, user_id=user_id, pk=pk)
        data = {
            'id': meeting.id,
            'title': meeting.title,
            'datetime': meeting.datetime.isoformat(),
            'done': meeting.done,
            'user_id': meeting.user_id
        }
        return JsonResponse(data)

    def patch(self, request, user_id, pk):
        try:
            meeting = get_object_or_404(Meeting, user_id=user_id, pk=pk)
            data = json.loads(request.body)
            print("Received patch data:", data)
            meeting.title = data.get('title', meeting.title)
            datetime_str = data.get('datetime', meeting.datetime.isoformat())
            if isinstance(datetime_str, str):
                meeting.datetime = datetime.fromisoformat(datetime_str)
            meeting.done = data.get('done', meeting.done)
            meeting.save()
            return JsonResponse({'message': 'Meeting updated successfully', 'meeting': {
                'id': meeting.id,
                'title': meeting.title,
                'datetime': meeting.datetime.isoformat(),
                'done': meeting.done,
                'user_id': meeting.user_id
            }})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
        except ValueError as ve:
            return JsonResponse({'error': f'Invalid datetime format: {ve}'}, status=400)

    def delete(self, request, user_id, pk):
        meeting = get_object_or_404(Meeting, user_id=user_id, pk=pk)
        meeting.delete()
        return JsonResponse({'message': 'Meeting deleted successfully'}, status=200)


@csrf_exempt
def meeting_list(request, user_id):
    if request.method == 'GET':
        meetings = Meeting.objects.filter(user_id=user_id)
        meetings_list = [
            {
                'id': meeting.id,
                'title': meeting.title,
                'datetime': meeting.datetime.isoformat(),
                'done': meeting.done,
                'user_id': meeting.user_id
            }
            for meeting in meetings
        ]
        return JsonResponse(meetings_list, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = get_object_or_404(User, id=user_id)
            
            datetime_str = data.get('datetime')
            meeting_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')

            meeting = Meeting.objects.create(
                user=user,
                title=data.get('title'),
                datetime=meeting_datetime,
                done=data.get('done', False)
            )
            return JsonResponse({
                'id': meeting.id,
                'title': meeting.title,
                'datetime': meeting.datetime.isoformat(),
                'done': meeting.done,
                'user_id': meeting.user_id
            }, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid datetime format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
