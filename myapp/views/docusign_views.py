import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import requests
from django.conf import settings

logger = logging.getLogger(__name__)

@csrf_exempt
def get_oauth_token(request):
    try:
        # Step 1: Request authorization code
        auth_url = (
            f"https://account-d.docusign.com/oauth/auth?response_type=code"
            f"&scope=signature"
            f"&client_id={settings.DOCUSIGN_INTEGRATION_KEY}"
            f"&redirect_uri={settings.DOCUSIGN_REDIRECT_URI}"
        )

        # Fetch the redirect URL using urllib
        with urllib.request.urlopen(auth_url) as response:
            redirected_url = response.geturl()  # Fetches the final URL after redirection
            logger.debug(f"Redirected URL: {redirected_url}")

        # Parse the authorization code from the URL
        parsed_url = urllib.parse.urlparse(redirected_url)
        authorization_code = urllib.parse.parse_qs(parsed_url.query).get('code')[0]
        logger.debug(f"Authorization code: {authorization_code}")

        # Step 2: Exchange the authorization code for an access token
        token_url = "https://account-d.docusign.com/oauth/token"
        base64_credentials = base64.b64encode(f"{settings.DOCUSIGN_INTEGRATION_KEY}:{settings.DOCUSIGN_SECRET_KEY}".encode('utf-8')).decode('utf-8')
        headers = {
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": authorization_code
        }

        token_response = requests.post(token_url, headers=headers, data=data)
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if access_token:
            return JsonResponse({'access_token': access_token})
        else:
            return JsonResponse({'error': 'Failed to retrieve access token', 'details': token_data}, status=400)

    except HTTPError as e:
        logger.error(f"HTTP error: {e.code} - {e.reason}")
        return JsonResponse({'error': f"HTTP error: {e.code} - {e.reason}"}, status=500)
    except URLError as e:
        logger.error(f"URL error: {e.reason}")
        return JsonResponse({'error': f"URL error: {e.reason}"}, status=500)
    except Exception as e:
        logger.error(f"Error in get_oauth_token: {e}")
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def get_authorization_code(request):
    try:
        # Define the authorization URL
        auth_url = (
            "https://account-d.docusign.com/oauth/auth"
            "?response_type=code"
            "&scope=signature"
            "&client_id=9638a832-3d8d-4c73-b8c4-0323ff3aa1a7"
            "&redirect_uri=https%3A%2F%2Foyster-app-vhznt.ondigitalocean.app"
            "&state=pY8wl6h04PardhgXHAQdmz746VHwzc"
        )

        # Fetch the redirect URL using urllib
        with urllib.request.urlopen(auth_url) as response:
            redirected_url = response.geturl()  # Fetches the final URL after redirection
            logger.debug(f"Redirected URL: {redirected_url}")

        # Parse the authorization code from the URL
        parsed_url = urllib.parse.urlparse(redirected_url)
        authorization_code = urllib.parse.parse_qs(parsed_url.query).get('code')[0]
        logger.debug(f"Authorization Code: {authorization_code}")

        # Return the authorization code in the response
        return JsonResponse({'authorization_code': authorization_code})

    except HTTPError as e:
        logger.error(f"HTTP error: {e.code} - {e.reason}")
        return JsonResponse({'error': f"HTTP error: {e.code} - {e.reason}"}, status=500)
    except URLError as e:
        logger.error(f"URL error: {e.reason}")
        return JsonResponse({'error': f"URL error: {e.reason}"}, status=500)
    except Exception as e:
        logger.error(f"Error in get_authorization_code: {e}")
        return JsonResponse({'error': str(e)}, status=500)