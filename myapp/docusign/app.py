import logging
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import pdfkit
import requests
from jinja2 import Template
from docusign_esign import ApiClient, EnvelopesApi, Document, Signer, SignHere, Tabs, Recipients, EnvelopeDefinition, RecipientViewRequest
import base64
import config
from .user_data import user_data  # Adjust the import based on your project structure

logging.basicConfig(level=logging.DEBUG)

def index(request):
    return HttpResponse("Welcome to the User API!")

def get_user(request, user_id):
    if user_id in user_data:
        return JsonResponse(user_data[user_id])
    else:
        return HttpResponseNotFound("User not found")




@csrf_exempt
def generate_and_sign(request):
    try:
        data = request.json()
        user_id = data.get('user_id')
        signer_email = data.get('signer_email')

        if not user_id or not signer_email:
            return HttpResponseBadRequest("Missing user_id or signer_email")

        user = user_data.get(user_id)
        if not user:
            return HttpResponseNotFound("User not found")

        # Populate template
        html_content = populate_template(user)

        # Generate PDF
        pdf_path = 'document.pdf'
        generate_pdf(html_content, pdf_path)

        # Create envelope and send for signing
        signer_name = f"{user['first_name']} {user['last_name']}"
        sign_url = create_embedded_signing_url(pdf_path, signer_email, signer_name)

        return JsonResponse({"sign_url": sign_url}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def oauth_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)

    token_url = f"{config.DOCUSIGN_ACCOUNT_BASE_URI}/oauth/token"
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': config.DOCUSIGN_INTEGRATION_KEY,
        'client_secret': config.DOCUSIGN_CLIENT_SECRET,
        'redirect_uri': config.DOCUSIGN_REDIRECT_URI
    }
    
    response = requests.post(token_url, data=data)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to obtain access token"}, status=response.status_code)

    token_info = response.json()
    config.DOCUSIGN_ACCESS_TOKEN = token_info['access_token']
    
    return JsonResponse({"message": "Authorization successful"}, status=200)

def populate_template(data):
    with open('template.html', 'r') as file:
        template = Template(file.read())
    return template.render(data)

def generate_pdf(html_content, output_path):
    pdfkit.from_string(html_content, output_path)

def create_embedded_signing_url(pdf_path, signer_email, signer_name):
    api_client = ApiClient()
    api_client.host = config.DOCUSIGN_ACCOUNT_BASE_URI + '/restapi'
    api_client.set_default_header("Authorization", "Bearer " + config.DOCUSIGN_ACCESS_TOKEN)

    envelopes_api = EnvelopesApi(api_client)
    envelope_definition = EnvelopeDefinition()
    envelope_definition.email_subject = 'Please sign this document'

    with open(pdf_path, 'rb') as file:
        content_bytes = file.read()

    document = Document(
        document_base64=base64.b64encode(content_bytes).decode('utf-8'),
        name='Example Document',
        file_extension='pdf',
        document_id='1'
    )

    signer = Signer(
        email=signer_email,
        name=signer_name,
        recipient_id='1',
        routing_order='1',
        client_user_id='1234'  # Unique client user ID for embedded signing
    )

    sign_here = SignHere(
        document_id='1',
        page_number='1',
        recipient_id='1',
        tab_label='SignHereTab',
        x_position='100',
        y_position='100'
    )

    signer.tabs = Tabs(sign_here_tabs=[sign_here])
    envelope_definition.documents = [document]
    envelope_definition.recipients = Recipients(signers=[signer])
    envelope_definition.status = 'sent'

    envelope_summary = envelopes_api.create_envelope(account_id=config.DOCUSIGN_API_ACCOUNT_ID, envelope_definition=envelope_definition)

    # Create the recipient view request object
    view_request = RecipientViewRequest(
        authentication_method='email',
        client_user_id='1234',  # Same as the client user ID used when creating the envelope
        recipient_id='1',
        return_url='http://localhost:5000/return',
        user_name=signer_name,
        email=signer_email
    )

    results = envelopes_api.create_recipient_view(
        account_id=config.DOCUSIGN_API_ACCOUNT_ID,
        envelope_id=envelope_summary.envelope_id,
        recipient_view_request=view_request
    )

    return results.url

def return_url(request):
    return HttpResponse("Thank you for signing the document!")

@csrf_exempt
def webhook(request):
    try:
        data = request.json()
        # Check the event type and envelope status
        if data.get('event') == 'envelope-completed':
            # Get the envelope ID
            envelope_id = data['envelopeId']
            # Download the completed document
            download_signed_document(envelope_id)
        return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def download_signed_document(envelope_id):
    api_client = ApiClient()
    api_client.host = config.DOCUSIGN_ACCOUNT_BASE_URI + '/restapi'
    api_client.set_default_header("Authorization", "Bearer " + config.DOCUSIGN_ACCESS_TOKEN)

    envelopes_api = EnvelopesApi(api_client)
    document_id = '1'  # Assuming a single document with ID 1
    signed_document = envelopes_api.get_document(
        account_id=config.DOCUSIGN_API_ACCOUNT_ID,
        envelope_id=envelope_id,
        document_id=document_id
    )

    with open('signed_document.pdf', 'wb') as f:
        f.write(signed_document)