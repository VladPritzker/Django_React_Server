import base64
import os
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from weasyprint import HTML
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Recipients
from django.http import JsonResponse
from django.conf import settings

@csrf_exempt
def convert_html_to_pdf_and_send(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
        except ParseError as e:
            return JsonResponse({"error": f"Invalid JSON - {str(e)}"}, status=400)
        
        email = data.get('email')
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # Path to the HTML template
        html_template_path = 'myapp/docusign/template.html'

        # Read the HTML template
        try:
            with open(html_template_path, 'r') as file:
                html_content = file.read()
        except FileNotFoundError:
            return JsonResponse({"error": "HTML template not found"}, status=500)

        # Convert HTML to PDF
        pdf_file_path = 'document.pdf'
        HTML(string=html_content).write_pdf(pdf_file_path)

        # Get DocuSign access token
        access_token = request.session.get('oauth_token', {}).get('access_token')
        if not access_token:
            return JsonResponse({"error": "DocuSign access token is missing"}, status=400)

        # Set up DocuSign API client
        api_client = ApiClient()
        api_client.host = settings.DOCUSIGN_ACCOUNT_BASE_URI + "/restapi"
        api_client.set_default_header("Authorization", "Bearer " + access_token)

        envelopes_api = EnvelopesApi(api_client)

        # Create the envelope
        with open(pdf_file_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()

        document_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        document = Document(
            document_base64=document_base64,
            name='Sample Document',
            file_extension='pdf',
            document_id='1'
        )

        signer = Signer(
            email=email,
            name='Recipient Name',
            recipient_id='1',
            routing_order='1'
        )

        sign_here = SignHere(
            document_id='1',
            page_number='1',
            recipient_id='1',
            tab_label='SignHereTab',
            x_position='100',
            y_position='100'
        )

        signer.tabs = {"sign_here_tabs": [sign_here]}
        recipients = Recipients(signers=[signer])
        envelope_definition = EnvelopeDefinition(
            email_subject="Please sign this document",
            documents=[document],
            recipients=recipients,
            status="sent"
        )

        result = envelopes_api.create_envelope(settings.DOCUSIGN_API_ACCOUNT_ID, envelope_definition=envelope_definition)

        return JsonResponse({"envelope_id": result.envelope_id}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=400)
