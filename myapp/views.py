from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import FinancialRecord, User, InvestingRecord, Note, MonthlyExpense, IncomeRecord, Contact
from datetime import datetime
import logging
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Sum
User = get_user_model()





logger = logging.getLogger(__name__)







@csrf_exempt
def users(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'register':
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            return JsonResponse({'message': 'User registered successfully', 'id': user.id}, status=201)

        elif action == 'login':
            user = authenticate(email=data.get('email'), password=data.get('password'))
            if user is not None:
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': float(user.money_invested),
                    'income_amount' : float(user.income_amount),
                    'money_spent': float(user.money_spent),
                    'balance': float(user.balance),
                    'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                    'spent_by_week': float(user.spent_by_week) if user.spent_by_week else None,
                    'spent_by_month': float(user.spent_by_month) if user.spent_by_month else None,
                    'spent_by_year': float(user.spent_by_year) if user.spent_by_year else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                }, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        elif action == 'fetch_user_details':
            user_id = data.get('user_id')
            try:
                user = User.objects.get(id=user_id)
                return JsonResponse({
                  'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': float(user.money_invested),
                    'income_amount' : float(user.income_amount),
                    'money_spent': float(user.money_spent),
                    'balance': float(user.balance),
                    'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                    'spent_by_week': float(user.spent_by_week) if user.spent_by_week else None,
                    'spent_by_month': float(user.spent_by_month) if user.spent_by_month else None,
                    'spent_by_year': float(user.spent_by_year) if user.spent_by_year else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

    elif request.method == 'GET':
        users = User.objects.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return JsonResponse(users_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    
    
@csrf_exempt
def usersData(request, user_id=None):
    if request.method == 'GET':
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                return JsonResponse({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'money_invested': float(user.money_invested),
                    'income_amount' : float(user.income_amount),
                    'money_spent': float(user.money_spent),
                    'balance': float(user.balance),
                    'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                    'spent_by_week': float(user.spent_by_week) if user.spent_by_week else None,
                    'spent_by_month': float(user.spent_by_month) if user.spent_by_month else None,
                    'spent_by_year': float(user.spent_by_year) if user.spent_by_year else None,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'photo': user.photo 
                })
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            users = User.objects.all()
            users_data = [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'money_invested': float(user.money_invested),
                'income_amount' : float(user.income_amount),
                'money_spent': float(user.money_spent),
                'balance': float(user.balance),
                'balance_goal': float(user.balance_goal) if user.balance_goal else None,
                'spent_by_week': float(user.spent_by_week) if user.spent_by_week else None,
                'spent_by_month': float(user.spent_by_month) if user.spent_by_month else None,
                'spent_by_year': float(user.spent_by_year) if user.spent_by_year else None,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser
            } for user in users]
            return JsonResponse(users_data, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        try:
            user = User.objects.create(**data)
            return JsonResponse({'message': 'User created successfully', 'id': user.id}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'PATCH':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for updates'}, status=400)
        try:
            data = json.loads(request.body)
            user = User.objects.get(pk=user_id)
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
            return JsonResponse({'message': 'User updated successfully'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'DELETE':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for deletion'}, status=400)
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
def financial_records(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            title = data.get('title')
            amount = data.get('amount')
            record_date = data.get('record_date')

            parsed_date = datetime.strptime(record_date, '%Y-%m-%d').date()
            user = User.objects.get(id=user_id)

            record = FinancialRecord.objects.create(
                user=user,
                title=title,
                amount=amount,
                record_date=parsed_date
            )
            return JsonResponse({
                'id': record.id,
                'user_id': record.user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat()
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as ve:
            return JsonResponse({'error': 'Date format error: ' + str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)

    elif request.method == 'GET':
        user_id = request.GET.get('user_id')
        records = FinancialRecord.objects.all()
        if user_id:
            records = records.filter(user_id=user_id)

        records_data = [
            {'id': record.id, 'user_id': record.user.id, 'record_date': record.record_date.isoformat(),
             'title': record.title, 'amount': float(record.amount)}
            for record in records
        ]
        return JsonResponse(records_data, safe=False)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_financial_record(request, user_id, record_id):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
            record = FinancialRecord.objects.get(id=record_id, user=user)
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except FinancialRecord.DoesNotExist:
            return JsonResponse({'error': 'Financial record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



    

    
@csrf_exempt
def investing_records(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        records = InvestingRecord.objects.filter(user_id=user_id) if user_id else InvestingRecord.objects.all()
        records_data = [
            {
                'id': record.id, 'user_id': record.user.id, 'title': record.title, 'amount': float(record.amount),
                'record_date': record.record_date.isoformat(), 'tenor': record.tenor, 'type_invest': record.type_invest,
                'amount_at_maturity': float(record.amount_at_maturity) if record.amount_at_maturity else None,  # New field
                'rate': float(record.rate) if record.rate else None  # New field
            }
            for record in records
        ]
        return JsonResponse(records_data, safe=False)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            record_id = data['id']
            record = InvestingRecord.objects.get(id=record_id)
            record.delete()
            return JsonResponse({'message': 'Record deleted successfully.'}, status=200)
        except InvestingRecord.DoesNotExist:
            return JsonResponse({'error': 'Record not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)
        
    elif request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ['user_id', 'title', 'amount', 'record_date', 'tenor', 'type_invest']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': 'Missing required fields: ' + ', '.join(missing_fields)}, status=400)

        try:
            user_id = data['user_id']
            user = User.objects.get(id=user_id)  # Ensure user exists

            record = InvestingRecord.objects.create(
                user=user,
                title=data['title'],
                amount=data['amount'],
                record_date=datetime.strptime(data['record_date'], '%Y-%m-%d').date(),
                tenor=data['tenor'],
                type_invest=data['type_invest'],
                amount_at_maturity=data.get('amount_at_maturity', None),  # New field
                rate=data.get('rate', None)  # New field
            )
            return JsonResponse({
                'id': record.id,
                'user_id': user.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat(),
                'tenor': record.tenor,
                'type_invest': record.type_invest,
                'amount_at_maturity': str(record.amount_at_maturity) if record.amount_at_maturity else None,  # New field
                'rate': str(record.rate) if record.rate else None  # New field
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except ValueError as ve:
            return JsonResponse({'error': 'Data format error: ' + str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Server error: ' + str(e)}, status=500)


@csrf_exempt
def notes(request, user_id=None):
    if request.method == 'GET':
        if user_id:
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

    elif request.method == 'POST':
        data = json.loads(request.body)
        required_fields = ['user_id', 'title', 'note', 'date', 'priority']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return JsonResponse({'error': 'Missing required fields: ' + ', '.join(missing_fields)}, status=400)

        try:
            user = User.objects.get(pk=data['user_id'])
            date = datetime.strptime(data['date'], '%Y-%m-%d').date()  # Ensure date is parsed correctly
            note = Note.objects.create(
                user=user,
                title=data['title'],
                note=data['note'],
                date=date,  # Set the parsed date
                priority=data['priority'],
                order=data.get('order', 0)  # Set the order if provided
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
            return JsonResponse({'error': 'Date format error: ' + str(e)}, status=400)  # Handle date parsing errors
        except Exception as e:
            return JsonResponse({'error': 'Failed to create note: ' + str(e)}, status=500)

    elif request.method == 'PATCH':
        data = json.loads(request.body)
        if user_id:
            try:
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
            except Note.DoesNotExist:
                return JsonResponse({'error': 'Note not found'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'User ID is required for reordering'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def note_detail_update(request, user_id, note_id):
    if request.method == 'GET':
        try:
            # Ensure the note belongs to the specified user
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
            # Update only the fields that are provided in the request body
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
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def monthly_expenses(request, user_id=None, expense_id=None):
    User = get_user_model()  # Use the custom user model defined in settings


    if request.method == 'GET':
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                expenses = MonthlyExpense.objects.filter(user=user)
                data = list(expenses.values('id', 'user_id', 'title', 'amount'))
                return JsonResponse(data, safe=False)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            return JsonResponse({'error': 'User ID is required'}, status=400)


    elif request.method == 'POST':
        if not user_id:
            return JsonResponse({'error': 'User ID is required for posting expenses'}, status=400)

        try:
            user = User.objects.get(pk=user_id)
            data = json.loads(request.body)
            monthly_expense = MonthlyExpense.objects.create(
                user=user,
                title=data['title'],
                amount=data['amount']
            )
            return JsonResponse({
                'id': monthly_expense.id,
                'user_id': monthly_expense.user_id,
                'title': monthly_expense.title,
                'amount': str(monthly_expense.amount)
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'DELETE':
        if not expense_id:
            return JsonResponse({'error': 'Expense ID is required for deletion'}, status=400)

        try:
            expense = MonthlyExpense.objects.get(pk=expense_id)
            expense.delete()
            return JsonResponse({'message': 'Expense deleted successfully'}, status=204)
        except MonthlyExpense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def expense_detail(request, user_id, expense_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    if request.method == 'GET':
        try:
            expense = MonthlyExpense.objects.get(user=user, id=expense_id)
            return JsonResponse({'id': expense.id, 'user_id': user.id, 'title': expense.title, 'amount': str(expense.amount)}, status=200)
        except MonthlyExpense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)

    elif request.method == 'PUT':
        try:
            expense = MonthlyExpense.objects.get(user=user, id=expense_id)
            data = json.loads(request.body)
            expense.title = data.get('title', expense.title)
            expense.amount = data.get('amount', expense.amount)
            expense.save()
            return JsonResponse({'id': expense.id, 'title': expense.title, 'amount': str(expense.amount)}, status=200)
        except MonthlyExpense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)

    elif request.method == 'DELETE':
        try:
            expense = MonthlyExpense.objects.get(user=user, id=expense_id)
            print(f"Deleting expense: {expense.title}, ID: {expense.id}")  # Debug print
            expense.delete()
            print("Deletion successful.")  # Confirm deletion
            return JsonResponse({'message': 'Expense deleted successfully'}, status=204)
        except MonthlyExpense.DoesNotExist:
            print("Expense not found for deletion.")  # Debug print
            return JsonResponse({'error': 'Expense not found'}, status=404)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    



@csrf_exempt
def upload_photo(request, user_id):
    if request.method == 'POST' and request.FILES.get('photo'):
        photo = request.FILES['photo']
        filename = f'user_{user_id}/{photo.name}'
        file_path = default_storage.save(filename, ContentFile(photo.read()))

        try:
            user = User.objects.get(pk=user_id)
            user.photo = file_path
            user.save()
            return JsonResponse({'file_url': file_path}, status=201)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)






def update_user_income(user):
    total_income = IncomeRecord.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0.00
    user.income_amount = total_income
    user.save()

@csrf_exempt
def income_records_view(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)

        if request.method == 'GET':
            income_records = IncomeRecord.objects.filter(user=user)
            records = [
                {
                    'id': record.id,
                    'title': record.title,
                    'amount': str(record.amount),
                    'record_date': record.record_date.isoformat()
                } for record in income_records
            ]
            return JsonResponse(records, safe=False, status=200)

        elif request.method == 'POST':
            data = json.loads(request.body)
            title = data.get('title')
            amount = data.get('amount')
            record_date = data.get('record_date')

            if not title or not amount or not record_date:
                return JsonResponse({'error': 'Missing fields'}, status=400)

            # Convert record_date from string to date object
            record_date = datetime.strptime(record_date, '%Y-%m-%d').date()

            record = IncomeRecord.objects.create(
                user=user,
                title=title,
                amount=amount,
                record_date=record_date
            )
            update_user_income(user)
            return JsonResponse({
                'id': record.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat()
            }, status=201)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def income_record_detail_view(request, user_id, record_id):
    try:
        user = get_object_or_404(User, id=user_id)
        record = get_object_or_404(IncomeRecord, id=record_id, user=user)

        if request.method == 'PATCH':
            data = json.loads(request.body)
            title = data.get('title', record.title)
            amount = data.get('amount', record.amount)
            record_date = data.get('record_date', record.record_date)

            if isinstance(record_date, str):
                # Convert record_date from string to date object if needed
                record_date = datetime.strptime(record_date, '%Y-%m-%d').date()

            record.title = title
            record.amount = amount
            record.record_date = record_date
            record.save()
            update_user_income(user)
            return JsonResponse({
                'id': record.id,
                'title': record.title,
                'amount': str(record.amount),
                'record_date': record.record_date.isoformat()
            }, status=200)
        elif request.method == 'DELETE':
            record.delete()
            update_user_income(user)
            return JsonResponse({'message': 'Record deleted'}, status=204)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
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
        return JsonResponse({'message': 'Contact deleted successfully'}, status=204)