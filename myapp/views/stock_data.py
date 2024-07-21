# views.py
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from myapp.models import StockData
from myapp.serializers import StockDataSerializer

@api_view(['GET', 'POST', 'DELETE'])
def stock_data_view(request):
    if request.method == 'GET':
        stock_data = StockData.objects.all()
        serializer = StockDataSerializer(stock_data, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        url = "https://api.stockdata.org/v1/data/quote?symbols=AAPL,TSLA,MSFT&api_token=" + settings.STOCK_DATA_KEY
        response = requests.get(url)
        if response.headers['Content-Type'] == 'application/json':
            data = response.json().get('data', [])

            # Clear existing data
            # StockData.objects.all().delete()

            # Prepare data for serialization
            stock_data_list = []
            for item in data:
                stock_data_list.append({
                    "ticker": item.get("ticker"),
                    "name": item.get("name"),
                    "price": item.get("price"),
                    "day_high": item.get("day_high"),
                    "day_low": item.get("day_low"),
                    "day_open": item.get("day_open"),
                    "week_52_high": item.get("52_week_high"),
                    "week_52_low": item.get("52_week_low"),
                    "previous_close_price": item.get("previous_close_price"),
                    "day_change": item.get("day_change"),
                    "volume": item.get("volume"),
                    "date": item.get("last_trade_time")
                })

            # Save new data to the database
            serializer = StockDataSerializer(data=stock_data_list, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'error': 'Invalid response from API', 'details': response.text}, status=500)

    elif request.method == 'DELETE':
        StockData.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
