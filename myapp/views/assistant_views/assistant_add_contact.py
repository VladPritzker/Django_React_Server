from myapp.models import Contact
from django.http import JsonResponse

def handle_contact_action(action_data, user_id):
    if not user_id:
        return JsonResponse({'error': 'User ID is missing'}, status=400)

    action = action_data.get('action')
    name = action_data.get('name')
    phone_number = action_data.get('phone_number')  # May be None for delete action

    if action == 'add_contact':
        if not name or not phone_number:
            return JsonResponse({'error': 'Name and phone number are required to add a contact.'}, status=400)
        contact, created = Contact.objects.get_or_create(
            user_id=user_id,
            name=name,
            defaults={'phone_number': phone_number}
        )
        if not created:
            return JsonResponse({'reply': f'Contact {name} already exists.'}, status=200)
        return JsonResponse({'reply': f'Contact {name} added successfully!'}, status=200)
    elif action == 'delete_contact':
        if not name:
            return JsonResponse({'error': 'Name is required to delete a contact.'}, status=400)
        contact = Contact.objects.filter(user_id=user_id, name=name).first()
        if contact:
            contact.delete()
            return JsonResponse({'reply': f'Contact {name} deleted successfully!'}, status=200)
        else:
            return JsonResponse({'reply': f'Contact {name} not found.'}, status=404)
    elif action == 'list_contacts':
        # Fetch the contacts for the user
        contacts = Contact.objects.filter(user_id=user_id)
        if not contacts.exists():
            return JsonResponse({'reply': 'You have no contacts.'}, status=200)
        # Format the contacts into a string
        reply = "Here are your contacts:\n"
        for contact in contacts:
            reply += f"- {contact.name}: {contact.phone_number}\n"
        return JsonResponse({'reply': reply}, status=200)

    else:
        return JsonResponse({'error': 'Invalid action specified.'}, status=400)
