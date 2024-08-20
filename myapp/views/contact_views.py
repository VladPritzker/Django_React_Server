from django.views.decorators.http import require_http_methods  # Add this import
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from myapp.models import Contact, User
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.utils.decorators import method_decorator
from django.views import View






@csrf_exempt
@require_http_methods(["GET", "POST"])
def contact_list(request, user_id):
    if request.method == 'GET':
        contacts = Contact.objects.filter(user_id=user_id)
        contact_list = [
            {
                'id': contact.id,
                'name': contact.name,
                'phone_number': contact.phone_number,
                'note': contact.note,
                'user_id': contact.user_id
            }
            for contact in contacts
        ]
        return JsonResponse(contact_list, safe=False)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user = get_object_or_404(User, id=user_id)
            contact = Contact.objects.create(
                user_id=user.id,
                name=data.get('name'),
                phone_number=data.get('phone_number'),
                note=data.get('note', '')
            )
            return JsonResponse({
                'id': contact.id,
                'name': contact.name,
                'phone_number': contact.phone_number,
                'note': contact.note,
                'user_id': contact.user_id
            }, status=201)
        except json.JSONDecodeError:
            logger.error("Invalid JSON received: %s", request.body)
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            logger.error("Missing field: %s in data: %s", e, data)
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)
        except Exception as e:
            logger.error("An error occurred: %s", e)
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ContactDetailView(View):

    def get(self, request, user_id, pk):
        contact = get_object_or_404(Contact, user_id=user_id, pk=pk)
        data = {
            'id': contact.id,
            'name': contact.name,
            'phone_number': contact.phone_number,
            'note': contact.note,
            'user_id': contact.user_id,
        }
        return JsonResponse(data)

    def patch(self, request, user_id, pk):
        try:
            contact = get_object_or_404(Contact, user_id=user_id, pk=pk)
            data = json.loads(request.body.decode('utf-8'))
            contact.name = data.get('name', contact.name)
            contact.phone_number = data.get('phone_number', contact.phone_number)
            contact.note = data.get('note', contact.note)
            contact.save()
            return JsonResponse({'message': 'Contact updated successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError as e:
            return JsonResponse({'error': f'Missing field: {e}'}, status=400)

    def delete(self, request, user_id, pk):
        contact = get_object_or_404(Contact, user_id=user_id, pk=pk)
        contact.delete()
        return JsonResponse({'message': 'Contact deleted successfully'}, status=200)