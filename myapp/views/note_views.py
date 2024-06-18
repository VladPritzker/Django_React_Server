from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import Note, User
from datetime import datetime
import json
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

@csrf_exempt
def notes(request, user_id=None):
    if request.method == 'GET':
        try:
            if user_id:
                notes = Note.objects.filter(user_id=user_id).order_by('order')
                if not notes.exists():
                    return JsonResponse({'error': 'Notes for the specified user not found'}, status=404)
            else:
                notes = Note.objects.all().order_by('order')
            
            notes_data = [
                {
                    'id': note.id,
                    'user_id': note.user.id,
                    'title': note.title,
                    'note': note.note,
                    'date': note.date.isoformat() if note.date else None,
                    'priority': note.priority,
                    'done': note.done,
                    'hide': note.hide,
                    'order': note.order
                } for note in notes
            ]
            return JsonResponse(notes_data, safe=False)
        except Exception as e:
            logger.error("Error fetching notes: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['user_id', 'title', 'note', 'date', 'priority']
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                return JsonResponse({'error': 'Missing required fields: ' + ', '.join(missing_fields)}, status=400)

            user = User.objects.get(pk=data['user_id'])
            date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            note = Note.objects.create(
                user=user,
                title=data['title'],
                note=data['note'],
                date=date,
                priority=data['priority'],
                order=data.get('order', 0)
            )
            return JsonResponse({
                'id': note.id,
                'user_id': note.user.id,
                'title': note.title,
                'note': note.note,
                'date': note.date.isoformat(),
                'priority': note.priority,
                'done': note.done,
                'hide': note.hide,
                'order': note.order
            }, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as e:
            return JsonResponse({'error': 'Date format error: ' + str(e)}, status=400)
        except Exception as e:
            logger.error("Error creating note: %s", str(e), exc_info=True)
            return JsonResponse({'error': 'Failed to create note: ' + str(e)}, status=500)

    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            if user_id:
                with transaction.atomic():
                    for note_data in data['notes']:
                        note = Note.objects.get(id=note_data['id'], user_id=user_id)
                        note.title = note_data.get('title', note.title)
                        note.note = note_data.get('note', note.note)
                        note.priority = note_data.get('priority', note.priority)
                        note.done = note_data.get('done', note.done)
                        note.hide = note_data.get('hide', note.hide)
                        note.order = note_data.get('order', note.order)
                        note.save()
                return JsonResponse({'message': 'Notes reordered successfully'}, status=200)
            else:
                return JsonResponse({'error': 'User ID is required for reordering'}, status=400)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Error reordering notes: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def note_detail_update(request, user_id, note_id):
    if request.method == 'GET':
        try:
            note = Note.objects.get(id=note_id, user_id=user_id)
            return JsonResponse({
                'id': note.id,
                'user_id': note.user.id,
                'title': note.title,
                'note': note.note,
                'date': note.date.isoformat() if note.date else None,
                'priority': note.priority,
                'done': note.done,
                'hide': note.hide,
                'order': note.order
            })
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)

    elif request.method == 'PATCH':
        try:
            note = Note.objects.get(id=note_id, user_id=user_id)
            data = json.loads(request.body)
            note.title = data.get('title', note.title)
            note.note = data.get('note', note.note)
            note.priority = data.get('priority', note.priority)
            note.done = data.get('done', note.done)
            note.hide = data.get('hide', note.hide)
            note.order = data.get('order', note.order)
            note.save()
            return JsonResponse({
                'id': note.id,
                'user_id': note.user.id,
                'title': note.title,
                'note': note.note,
                'date': note.date.isoformat() if note.date else None,
                'priority': note.priority,
                'done': note.done,
                'hide': note.hide,
                'order': note.order
            }, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Error updating note: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def reorder_notes(request, user_id):
    if request.method == 'GET':
        try:
            notes = Note.objects.filter(user_id=user_id).order_by('order')
            notes_data = [
                {
                    'id': note.id,
                    'user_id': note.user.id,
                    'title': note.title,
                    'note': note.note,
                    'date': note.date.isoformat() if note.date else None,
                    'priority': note.priority,
                    'done': note.done,
                    'hide': note.hide,
                    'order': note.order
                } for note in notes
            ]
            return JsonResponse(notes_data, safe=False)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Notes for the specified user not found'}, status=404)
        except Exception as e:
            logger.error("Error fetching reordered notes: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method == 'PATCH':
        try:
            data = json.loads(request.body)
            for item in data:
                note = Note.objects.get(id=item['id'], user_id=user_id)
                note.order = item['order']
                note.save()
            return JsonResponse({'message': 'Notes reordered successfully'}, status=200)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            logger.error("Error reordering notes: %s", str(e), exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
