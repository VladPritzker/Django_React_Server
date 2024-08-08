import os
import base64
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from weasyprint import HTML
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Document, Signer, SignHere, Recipients
from django.http import JsonResponse
from django.conf import settings

logger = logging.getLogger(__name__)

@csrf_exempt
def convert_html_to_pdf_and_send(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            logger.debug(f"Parsed data: {data}")
        except ParseError as e:
            logger.error(f"JSON parse error: {e}")
            return JsonResponse({"error": f"Invalid JSON - {str(e)}"}, status=400)

        email = data.get('email')
        if not email:
            logger.error("Email is required")
            return JsonResponse({"error": "Email is required"}, status=400)

        # Set the correct path for the HTML template
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        html_template_path = os.path.join(base_dir, 'myapp', 'docusign', 'template.html')

        try:
            with open(html_template_path, 'r') as file:
                html_content = file.read()
                logger.debug("HTML template read successfully")
        except FileNotFoundError:
            logger.error("HTML template not found")
            return JsonResponse({"error": "HTML template not found"}, status=500)

        pdf_file_path = 'document.pdf'
        try:
            HTML(string=html_content).write_pdf(pdf_file_path)
            logger.debug("HTML converted to PDF successfully")
        except Exception as e:
            logger.error(f"Failed to convert HTML to PDF: {e}")
            return JsonResponse({"error": f"Failed to convert HTML to PDF - {str(e)}"}, status=500)

        logger.debug(f"Session data: {request.session.items()}")

        access_token = request.session.get('oauth_token', {}).get('access_token')
        if not access_token:
            logger.error("DocuSign access token is missing")
            return JsonResponse({"error": "DocuSign access token is missing"}, status=400)

        try:
            api_client = ApiClient()
            api_client.host = settings.DOCUSIGN_ACCOUNT_BASE_URI + "/restapi"
            api_client.set_default_header("Authorization", "Bearer " + access_token)
            logger.debug("DocuSign API client configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure DocuSign API client: {e}")
            return JsonResponse({"error": f"Failed to configure DocuSign API client - {str(e)}"}, status=500)

        envelopes_api = EnvelopesApi(api_client)

        try:
            with open(pdf_file_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                logger.debug("PDF file read successfully")

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
            logger.debug(f"Envelope created successfully: {result.envelope_id}")

            return JsonResponse({"envelope_id": result.envelope_id}, status=200)
        except Exception as e:
            logger.error(f"Failed to create DocuSign envelope: {e}")
            return JsonResponse({"error": f"Failed to create DocuSign envelope - {str(e)}"}, status=500)

    logger.error("Invalid request method")
    return JsonResponse({"error": "Invalid request method"}, status=400)
