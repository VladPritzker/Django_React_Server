# myapp/views.py
from django.http import FileResponse, Http404
import os
from django.conf import settings

def download_pdf(request, envelope_id):
    file_name = f'envelope_{envelope_id}_combined.pdf'
    file_path = os.path.join(settings.BASE_DIR, 'envelopes', file_name)

    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response
    else:
        raise Http404("File not found")
