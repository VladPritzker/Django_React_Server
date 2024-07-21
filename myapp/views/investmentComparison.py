from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import InvestmentComparison
import json

@csrf_exempt
def investment_view(request, user_id=None, id=None):
    if request.method == 'GET':
        if id:
            investment = get_object_or_404(InvestmentComparison, id=id, user_id=user_id)
            return JsonResponse(model_to_dict(investment))
        else:
            investments = InvestmentComparison.objects.filter(user_id=user_id).values()
            return JsonResponse(list(investments), safe=False)
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        investment = InvestmentComparison.objects.create(user_id=user_id, **data)
        return JsonResponse(model_to_dict(investment), status=201)
    
    elif request.method == 'PATCH':
        data = json.loads(request.body)
        investment = get_object_or_404(InvestmentComparison, id=id, user_id=user_id)
        for key, value in data.items():
            setattr(investment, key, value)
        investment.save()
        return JsonResponse(model_to_dict(investment))
    
    elif request.method == 'DELETE':
        investment = get_object_or_404(InvestmentComparison, id=id, user_id=user_id)
        investment.delete()
        return JsonResponse({'message': 'Investment deleted'}, status=204)

def model_to_dict(model_instance):
    return {field.name: getattr(model_instance, field.name) for field in model_instance._meta.fields}
