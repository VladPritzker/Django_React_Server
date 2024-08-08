import logging
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session
from django.conf import settings
from django.http import JsonResponse

logger = logging.getLogger(__name__)

DOCUSIGN_AUTHORIZATION_URL = "https://account.docusign.com/oauth/auth"
DOCUSIGN_TOKEN_URL = "https://account.docusign.com/oauth/token"
CLIENT_ID = settings.DOCUSIGN_INTEGRATION_KEY
CLIENT_SECRET = settings.DOCUSIGN_SECRET_KEY
REDIRECT_URI = settings.DOCUSIGN_REDIRECT_URI
SCOPE = ["signature", "impersonation"]

def get_oauth_session(state=None, token=None):
    return OAuth2Session(
        CLIENT_ID,
        state=state,
        token=token,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE
    )

def docusign_login(request):
    oauth = get_oauth_session()
    authorization_url, state = oauth.authorization_url(DOCUSIGN_AUTHORIZATION_URL)
    request.session['oauth_state'] = state
    return redirect(authorization_url)

def docusign_callback(request):
    oauth = get_oauth_session(state=request.session['oauth_state'])
    token = oauth.fetch_token(
        DOCUSIGN_TOKEN_URL,
        authorization_response=request.build_absolute_uri(),
        client_secret=CLIENT_SECRET
    )
    request.session['oauth_token'] = token
    logger.debug(f"Token stored in session: {request.session['oauth_token']}")
    return JsonResponse(token)
