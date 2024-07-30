import requests
from io import BytesIO
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

API_URL = "https://api.stockdata.org/v1/news/all"
API_TOKEN = "qzjdITUayHMQ7cTBBBVHA79eNIplWJsVLM6ef4kg"

def fetch_stock_data(request):
    symbols = request.GET.get('symbols', 'TSLA,AMZN,MSFT')
    url = f"{API_URL}?symbols={symbols}&filter_entities=true&language=en&api_token={API_TOKEN}"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)

@csrf_exempt
def generate_pdf(request):
    if request.method == 'POST':
        data = json.loads(request.body).get('data')
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Stock Data")
        
        y = 700
        for item in data:
            p.drawString(100, y, f"Title: {item['title']}")
            y -= 15
            p.drawString(100, y, f"Description: {item['description']}")
            y -= 15
            p.drawString(100, y, f"URL: {item['url']}")
            y -= 30
            if y < 100:
                p.showPage()
                y = 750
        
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="stock_data.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)