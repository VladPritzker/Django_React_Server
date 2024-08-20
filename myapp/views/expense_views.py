from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from myapp.models import MonthlyExpense, User
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model

@csrf_exempt
@require_http_methods(["GET", "POST", "DELETE"])
def monthly_expenses(request, user_id=None, expense_id=None):
    User = get_user_model()

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
            return JsonResponse({'message': 'Expense deleted successfully'}, status=200)
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
            expense.delete()
            return JsonResponse({'message': 'Expense deleted successfully'}, status=200)
        except MonthlyExpense.DoesNotExist:
            return JsonResponse({'error': 'Expense not found'}, status=404)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
