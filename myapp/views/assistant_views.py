import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.models import Contact, User
from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)

@csrf_exempt
def assistant_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        messages = data.get('messages', [])
        user_id = data.get('user_id', None)

        # Convert messages to OpenAI format
        openai_messages = []
        for msg in messages:
            role = 'assistant' if msg['sender'] == 'assistant' else 'user'
            openai_messages.append({"role": role, "content": msg['text']})

        try:
            openai.api_key = settings.OPENAI_API_KEY

            # Check if the user message contains specific instructions for managing contacts
            if "add contact" in user_message.lower():
                return handle_add_contact(user_message, user_id)
            elif "delete contact" in user_message.lower():
                return handle_delete_contact(user_message, user_id)

            # For general queries, use the OpenAI API to generate a response
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=openai_messages,
                max_tokens=300,
                temperature=0.7,
            )
            assistant_reply = response['choices'][0]['message']['content'].strip()
            return JsonResponse({'reply': assistant_reply})

        except openai.error.OpenAIError as e:
            error_message = str(e)
            logger.error(f"OpenAI API error: {error_message}")
            return JsonResponse({'error': f'OpenAI API error: {error_message}'}, status=500)

        except Exception as e:
            logger.exception("Unexpected error:")
            return JsonResponse({'error': f'An internal server error occurred: {str(e)}'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

# Helper function to add a contact based on user's message
def handle_add_contact(user_message, user_id):
    try:
        # Example message: "Add contact John Doe, 1234567890"
        parts = user_message.split(',')
        name = parts[0].split('Add contact')[1].strip()
        phone_number = parts[1].strip()
        
        # Create a new contact
        user = get_object_or_404(User, id=user_id)
        contact = Contact.objects.create(user=user, name=name, phone_number=phone_number)
        
        return JsonResponse({
            'message': f'Contact {name} added successfully!',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'phone_number': contact.phone_number,
            }
        }, status=200)
    except Exception as e:
        logger.error(f"Error adding contact: {e}")
        return JsonResponse({'error': f'Error adding contact: {str(e)}'}, status=500)

# Helper function to delete a contact based on user's message
def handle_delete_contact(user_message, user_id):
    try:
        # Example message: "Delete contact John Doe"
        name = user_message.split('Delete contact')[1].strip()

        # Find and delete the contact by name
        contact = Contact.objects.filter(user_id=user_id, name=name).first()
        if contact:
            contact.delete()
            return JsonResponse({'message': f'Contact {name} deleted successfully!'}, status=200)
        else:
            return JsonResponse({'error': f'Contact {name} not found.'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        return JsonResponse({'error': f'Error deleting contact: {str(e)}'}, status=500)
