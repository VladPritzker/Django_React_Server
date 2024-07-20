# finance_views.py

import requests
from django.conf import settings
from django.http import JsonResponse

def get_stock_data(request):
    url = "https://api.stockdata.org/v1/data/quote?symbols=AAPL,TSLA,MSFT&api_token=" + settings.STOCK_DATA_KEY
    response = requests.get(url)
    if response.headers['Content-Type'] == 'application/json':
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Invalid response from API', 'details': response.text}, status=500)
