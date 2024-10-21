import openai
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from myapp.views.assistant_views.assistant_add_contact import handle_contact_action
from myapp.views.assistant_views.assistant_income import handle_income_action  # Import this
from myapp.views.assistant_views.assistant_spending import handle_spending_action  # Import this
from myapp.models import FinancialRecord, User  # Import models for financial records and user
from datetime import datetime
from decimal import Decimal

logger = logging.getLogger(__name__)

@csrf_exempt
def assistant_views(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        messages = data.get('messages', [])
        user_id = data.get('user_id', None)

        system_prompt = """
            You are a helpful assistant integrated into a user application that manages contacts, income, and spending records.
            When a user wants to add, delete, or list their contacts, income, or spending records, extract the intent and details.
            Respond in the following JSON format without additional text:

            {
                "action": "add_contact" or "delete_contact" or "list_contacts" or "add_income" or "list_income" or "add_spending" or "list_spending",
                "name": "Contact Name or Income/Spending Title",  // Include for adding or deleting contacts, income, or spending records
                "phone_number": "Phone Number",                  // Include only for adding contacts
                "amount": "Income or Spending Amount",           // Include for adding income or spending records
                "record_date": "Date (YYYY-MM-DD)"               // Include for adding income or spending records
            }

                If the user requests to add income or spending records but doesn't provide a `record_date`, show the following warning:
                "Please provide a date for the income or spending record in the format YYYY-MM-DD."
                If the user's request does not involve any listed actions, answer normally (not in json format).
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

                # Check for add_income or add_spending actions without record_date
                if action in ['add_income', 'add_spending']:
                    record_date = action_data.get('record_date')
                    if not record_date:
                        # Return a warning if the date is missing
                        return JsonResponse({'warning': 'Please include a date when adding income or spending.'}, status=400)
                
                # Proceed with the actual action handling
                if action in ['add_contact', 'delete_contact', 'list_contacts']:
                    return handle_contact_action(action_data, user_id)
                elif action in ['add_income', 'list_income']:
                    return handle_income_action(action_data, user_id)
                elif action in ['add_spending', 'list_spending']:
                    return handle_spending_action(action_data, user_id)  # Handle spending actions
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