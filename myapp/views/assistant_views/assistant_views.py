import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.views.assistant_views.assistant_add_contact import handle_contact_action
from myapp.views.assistant_views.assistant_income import handle_income_action  # Import this


logger = logging.getLogger(__name__)

@csrf_exempt
def assistant_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        messages = data.get('messages', [])
        user_id = data.get('user_id', None)

        system_prompt = """
        You are a helpful assistant integrated into a user application that manages contacts and income records.
        When a user wants to add, delete, or list their contacts or income records, extract the intent and details.
        Respond in the following JSON format without additional text:
        
        {
          "action": "add_contact" or "delete_contact" or "list_contacts" or "add_income" or "list_income",
          "name": "Contact Name or Income Title",  // Include for adding or deleting contacts or income
          "phone_number": "Phone Number",          // Include only for adding contacts
          "amount": "Income Amount",               // Include only for adding income records
          "record_date": "Date (YYYY-MM-DD)"       // Include only for adding income records
        }
        
        If the user's request does not involve any listed above actions, answer normally, means not in json format.
        """

                
        # Convert messages to OpenAI format
        openai_messages = [{"role": "system", "content": system_prompt}]
        for msg in messages:
            role = 'assistant' if msg['sender'] == 'assistant' else 'user'
            openai_messages.append({"role": role, "content": msg['text']})

        try:
            openai.api_key = settings.OPENAI_API_KEY

            # Call OpenAI API with the updated messages
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=openai_messages,
                max_tokens=300,
                temperature=0.7,
            )
            assistant_reply = response['choices'][0]['message']['content'].strip()

            # Try parsing the assistant's reply as JSON
            try:
                action_data = json.loads(assistant_reply)
                action = action_data.get('action')
                if action in ['add_contact', 'delete_contact', 'list_contacts']:
                    return handle_contact_action(action_data, user_id)
                elif action in ['add_income', 'list_income']:
                    return handle_income_action(action_data, user_id)
                else:
                    return JsonResponse({'error': 'Invalid action specified.'}, status=400)
            except json.JSONDecodeError:
                # If parsing fails, assume it's a general response
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
