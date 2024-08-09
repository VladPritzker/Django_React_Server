import base64
import logging
import time
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def get_oauth_token(request):
    # Step 1: Request authorization code
    auth_url = (
        f"https://account-d.docusign.com/oauth/auth?response_type=code"
        f"&scope=signature"
        f"&client_id={settings.DOCUSIGN_INTEGRATION_KEY}"
        f"&redirect_uri={settings.DOCUSIGN_REDIRECT_URI}"
    )
    
    # Set up headless browser using Selenium
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the authorization URL
    driver.get(auth_url)
    
    # Wait for the redirection (you might need to handle login here if required)
    time.sleep(10)  # Adjust the sleep time based on the actual redirection time
    
    # Get the current URL after redirection
    current_url = driver.current_url
    logger.debug(f"Redirected URL: {current_url}")

    # Parse the authorization code from the URL
    parsed_url = urlparse(current_url)
    authorization_code = parse_qs(parsed_url.query).get('code')[0]
    
    # Clean up the browser session
    driver.quit()
    
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
    access_token = token_data['access_token']
    
    return JsonResponse({'access_token': access_token})
