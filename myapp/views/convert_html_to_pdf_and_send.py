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

        # Inline HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>BHI Bank Onboarding for John Doe</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f4f4f4;
                }
                .container {
                    max-width: 800px;
                    margin: auto;
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #333;
                }
                p {
                    line-height: 1.6;
                }
                .section-title {
                    margin-top: 20px;
                    font-weight: bold;
                    color: #333;
                }
                .user-info {
                    margin: 10px 0;
                }
                .user-info span {
                    font-weight: bold;
                }
                .signature-section {
                    margin-top: 40px;
                    text-align: center;
                }
                .signature-placeholder {
                    border: 2px dashed #ccc;
                    padding: 20px;
                    margin-top: 20px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>BHI Bank Onboarding</h1>
                <p class="section-title">User Information:</p>
                <div class="user-info"><span>Organization:</span> BHI Bank</div>
                <div class="user-info"><span>First Name:</span> John</div>
                <div class="user-info"><span>Last Name:</span> Doe</div>
                <div class="user-info"><span>Customer Since:</span> 2020-01-01</div>
                <div class="user-info"><span>Relationship:</span> Client</div>
                <div class="user-info"><span>Street:</span> 123 Main St</div>
                <div class="user-info"><span>City:</span> New York</div>
                <div class="user-info"><span>Zipcode:</span> 10001</div>
                <div class="user-info"><span>Country:</span> USA</div>
                <div class="user-info"><span>Phone Type:</span> Mobile</div>
                <div class="user-info"><span>Tax ID:</span> 123-45-6789</div>
                <div class="user-info"><span>Email:</span> john.doe@example.com</div>
                <div class="user-info"><span>Political Exposure:</span> None</div>
                <div class="user-info"><span>Alias:</span> JD</div>

                <div class="signature-section">
                    <p class="section-title">Signature:</p>
                    <div class="signature-placeholder">
                        <!-- DocuSign Signature Placeholder -->
                        <p>Signature: /s1/</p>
                        <p>Date: /d1/</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

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
