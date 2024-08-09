import base64
import logging
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from requests_oauthlib import OAuth2Session
import requests
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

DOCUSIGN_AUTHORIZATION_URL = "https://account-d.docusign.com/oauth/auth"
DOCUSIGN_TOKEN_URL = "https://account-d.docusign.com/oauth/token"
CLIENT_ID = settings.DOCUSIGN_INTEGRATION_KEY
CLIENT_SECRET = settings.DOCUSIGN_SECRET_KEY
REDIRECT_URI = settings.DOCUSIGN_REDIRECT_URI
SCOPE = ["signature"]

def docusign_login(request):
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(DOCUSIGN_AUTHORIZATION_URL)
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def docusign_callback(request):
    code = request.GET.get('code')
    if not code:
        return JsonResponse({"error": "Authorization code not found in redirect URL"}, status=400)
    
    basic_auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    
    token_request_payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Authorization": f"Basic {basic_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(DOCUSIGN_TOKEN_URL, data=token_request_payload, headers=headers)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to obtain access token", "details": response.json()}, status=response.status_code)
    
    token_data = response.json()
    request.session['oauth_token'] = token_data

    return JsonResponse(token_data)

def send_envelope(request):
    token = request.session.get('oauth_token', {}).get('access_token')
    if not token:
        return redirect('docusign_login')  # Redirect to login if no token is found

    api_client = ApiClient()
    api_client.host = settings.DOCUSIGN_ACCOUNT_BASE_URI + "/restapi"
    api_client.set_default_header("Authorization", "Bearer " + token)

    envelopes_api = EnvelopesApi(api_client)

    # Your HTML content to convert to PDF
    html_content = """..."""

    pdf_file_path = 'document.pdf'
    HTML(string=html_content).write_pdf(pdf_file_path)

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
        email='recipient@example.com',
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
    return JsonResponse({"envelope_id": result.envelope_id})

# URL patterns:
# path('docusign/login/', docusign_login, name='docusign_login'),
# path('docusign/oauth/callback/', docusign_callback, name='docusign_callback'),
# path('docusign/send/', send_envelope, name='send_envelope'),
