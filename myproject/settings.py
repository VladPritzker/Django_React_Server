# settings.py

import os
from pathlib import Path
from datetime import timedelta

# Third-party libraries
from decouple import config
from dotenv import load_dotenv
import environ

# ----------------------------------------------------------
# JWT Settings
# ----------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': SECRET_KEY,  # Uncomment if you want to set a custom signing key
}

LOGIN_URL = 'https://pritzker-finance.com/'  # Update with your appropriate login URL

# ----------------------------------------------------------
# Environment & Base Directory
# ----------------------------------------------------------
# The environment variable DJANGO_ENV can be "development", "production", or "ci" (for GitLab CI, etc.)
DJANGO_ENV = os.getenv('DJANGO_ENV')

# Load variables from .env (if any)
load_dotenv()

# If you use django-environ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env()

# Decide BASE_URL by environment
BASE_URL = (
    config('BASE_URL', default="http://127.0.0.1:8000")
    if DJANGO_ENV == "development"
    else "https://oyster-app-vhznt.ondigitalocean.app"
)

# ----------------------------------------------------------
# SECRET KEY
# ----------------------------------------------------------
SECRET_KEY = config('SECRET_KEY')

# ----------------------------------------------------------
# DEBUG and SESSION Settings
# ----------------------------------------------------------
# (Adjust these in production!)
SESSION_COOKIE_SAMESITE = 'None'  # Options: 'Lax', 'Strict', 'None'
SESSION_COOKIE_SECURE = False     # Set True in production w/ HTTPS

# ----------------------------------------------------------
# ALLOWED HOSTS
# ----------------------------------------------------------
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'oyster-app-vhznt.ondigitalocean.app',
    'clownfish-app-dsl46.ondigitalocean.app',
    'http://localhost:3000',
    'http://pritzker-finance.com',
    'http://127.0.0.1:8081',
    # Apple / external hosts you listed
    'fpinit.itunes.apple.com',
    'westus-0.in.applicationinsights.azure.com',
    'mobile.events.data.microsoft.com',
    'dns.google',
    'mdbxgxqa.api.lncldglobal.com',
    'gspe35-ssl.ls.apple.com',
    'freedom.to',
    'gs-loc.apple.com',
    'mobile.events.data.microsoft.com',
    'gspe1-ssl.ls.apple.com',
    'copilot-telemetry.githubusercontent.com',
    'metrics.icloud.com',
]

# ----------------------------------------------------------
# CORS & CSRF
# ----------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://clownfish-app-dsl46.ondigitalocean.app',
    'https://oyster-app-vhznt.ondigitalocean.app',
    'http://pritzker-finance.com',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'https://clownfish-app-dsl46.ondigitalocean.app',
    'https://oyster-app-vhznt.ondigitalocean.app',
    'http://pritzker-finance.com',
    'http://copilot-telemetry.githubusercontent.com',
    'http://gateway.icloud.com'
]

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'
]

# ----------------------------------------------------------
# Django Apps & Middleware
# ----------------------------------------------------------
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'myapp',
    'storages',
    'anymail',
    'sendgrid_backend',
]

ANYMAIL = {
    'MAILGUN_API_KEY': 'your-mailgun-api-key',
    'MAILGUN_SENDER_DOMAIN': 'your-domain.com',  # e.g., mg.your-domain.com
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myapp.middleware.ResetDBTableMiddleware',
]

AUTH_USER_MODEL = 'myapp.User'  # Custom user model

ROOT_URLCONF = 'myproject.urls'

# For your local filesystem path
BASE_DIR = '/Users/vladbuzhor/Library/Mobile Documents/com~apple~CloudDocs/Vlad/Study/Study/Django_Angular_React_finance/Django_server'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '/Users/vladbuzhor/Library/Mobile Documents/com~apple~CloudDocs/Vlad/Study/Study/Django_Angular_React_finance/Django_server/myapp/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# ----------------------------------------------------------
# Database Logic
#   - If DJANGO_ENV=ci, force DB_HOST='mysql'
#   - Otherwise read from .env or fallback to '127.0.0.1'
# ----------------------------------------------------------
if os.getenv('DJANGO_ENV') == 'ci':
    DB_HOST = 'mysql'
else:
    DB_HOST = config('DB_HOST', default='127.0.0.1')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': DB_HOST,
        'PORT': config('DB_PORT', default=3306, cast=int),
    }
}

# ----------------------------------------------------------
# Password Validation
# ----------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ----------------------------------------------------------
# Logging
# ----------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# ----------------------------------------------------------
# i18n and TZ
# ----------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_TZ = True  # or False if you'd prefer

# ----------------------------------------------------------
# Static Files
# ----------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

USE_TZ = False  # You mentioned you set it to False

# ----------------------------------------------------------
# File Storage
# ----------------------------------------------------------
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# ----------------------------------------------------------
# Email & SendGrid
# ----------------------------------------------------------
EMAIL_BACKEND = 'django_sendgrid_v5.backend.SendgridBackend'
DEFAULT_FROM_EMAIL = 'pritzkervlad@gmail.com'
SERVER_EMAIL = 'https://oyster-app-vhznt.ondigitalocean.app@pritzker-finance.com'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # Ensure this line is set to False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# ----------------------------------------------------------
# Additional Keys & Credentials
# ----------------------------------------------------------
STOCK_DATA_KEY = config('STOCK_DATA_KEY')

OPENAI_API_KEY = config('REACT_APP_OPENAI_API_KEY')

# DocuSign
DOCUSIGN_CLIENT_ID = config('DOCUSIGN_CLIENT_ID')
DOCUSIGN_CLIENT_SECRET = config('DOCUSIGN_CLIENT_SECRET')
DOCUSIGN_ACCOUNT_ID = config('DOCUSIGN_ACCOUNT_ID')
DOCUSIGN_TEMPLATE_ID = config('DOCUSIGN_TEMPLATE_ID')
DOCUSIGN_ACCESS_TOKEN = config('DOCUSIGN_ACCESS_TOKEN')
# DOCUSIGN_REFRESH_TOKEN = config('DOCUSIGN_REFRESH_TOKEN')

# Plaid
PLAID_ENV = env('PLAID_ENV', default='sandbox')
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID', '66fda6e6e90824001ac9f646')
PLAID_SECRET = os.getenv('PLAID_SECRET', '8c0e67c007c2b48e98a2499652f982')
PLAID_SANDBOX_SECRET = os.getenv('PLAID_SANDBOX_SECRET', 'b975402f6416411b11fb5a86f4eb39')

# ----------------------------------------------------------
# Password Reset Timeout
# ----------------------------------------------------------
PASSWORD_RESET_TIMEOUT = 86400  # 1 day

# ----------------------------------------------------------
# DigitalOcean Spaces Config
# ----------------------------------------------------------
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DIGITALOCEAN_STORAGE_BUCKET_NAME = 'photopritzkerinance'
DIGITALOCEAN_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = DIGITALOCEAN_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = DIGITALOCEAN_ENDPOINT_URL
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read',  # Files publicly readable by default
}
AWS_QUERYSTRING_AUTH = False
AWS_LOCATION = ''
AWS_DEFAULT_ACL = None