from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    driver = None  # Initialize driver to None
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

        # Set up Selenium WebDriver with Chrome in headless mode
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Open the authorization URL
        driver.get(auth_url)

        # Wait for the authorization code to be in the URL after the redirection
        WebDriverWait(driver, 20).until(
            EC.url_contains("code=")
        )

        # Get the current URL after the final redirection
        redirected_url = driver.current_url
        logger.debug(f"Redirected URL: {redirected_url}")

        # Parse the authorization code from the URL
        parsed_url = urlparse(redirected_url)
        code_list = parse_qs(parsed_url.query).get('code')

        if code_list:
            authorization_code = code_list[0]
            logger.debug(f"Authorization Code: {authorization_code}")
            return JsonResponse({'authorization_code': authorization_code})
        else:
            logger.error("Authorization code not found in the redirected URL.")
            return JsonResponse({'error': 'Authorization code not found'}, status=400)

    except Exception as e:
        logger.error(f"Error in get_authorization_code: {e}")
        return JsonResponse({'error': str(e)}, status=500)