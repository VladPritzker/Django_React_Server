# settings.py
import os
from pathlib import Path
from decouple import config
from dotenv import load_dotenv
LOGIN_URL = 'https://pritzker-finance.com/'  # Update with the correct login URL




# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
SESSION_COOKIE_SAMESITE = 'None'  # Options: 'Lax', 'Strict', 'None'
SESSION_COOKIE_SECURE = False   # Set to True in production with HTTPS


# Allowed hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'oyster-app-vhznt.ondigitalocean.app',  # Production
    'clownfish-app-dsl46.ondigitalocean.app',
    'http://localhost:3000',
    'http://pritzker-finance.com',
    'http://127.0.0.1:8081'
 
]

# CORS and CSRF settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # Local frontend
    'https://clownfish-app-dsl46.ondigitalocean.app',  # Production frontend
    'https://oyster-app-vhznt.ondigitalocean.app',  # Production backend
    'http://pritzker-finance.com',
    
 
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # Local frontend
    'https://clownfish-app-dsl46.ondigitalocean.app',  # Production frontend
    'https://oyster-app-vhznt.ondigitalocean.app',  # Production backend
    'http://pritzker-finance.com'
]
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = True



AUTH_USER_MODEL = 'myapp.User'

# Application definition
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
    'myapp',
    'storages'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS handling should be very early, before most other middlewares
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myapp.middleware.ResetDBTableMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myapp/templates')],  # Ensure this path is correct
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

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')




# Ensure you have the correct storage backend set up
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Additional settings
USE_TZ = False
CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False  # Ensure this line is set to False
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'no-reply@pritzker-finance.com'

STOCK_DATA_KEY = config('STOCK_DATA_KEY')
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS'
]
## openAI
OPENAI_API_KEY = config('REACT_APP_OPENAI_API_KEY')

## docusign
DOCUSIGN_CLIENT_ID = config('DOCUSIGN_CLIENT_ID')
DOCUSIGN_CLIENT_SECRET = config('DOCUSIGN_CLIENT_SECRET')
DOCUSIGN_ACCOUNT_ID = config('DOCUSIGN_ACCOUNT_ID')
DOCUSIGN_TEMPLATE_ID = config('DOCUSIGN_TEMPLATE_ID')
DOCUSIGN_ACCESS_TOKEN = config('DOCUSIGN_ACCESS_TOKEN')
# DOCUSIGN_REFRESH_TOKEN = config('DOCUSIGN_REFRESH_TOKEN')


## Plaid
PLAID_CLIENT_ID = config('PLAID_CLIENT_ID')
PLAID_SECRET = config('PLAID_SECRET')
PLAID_HOST = 'https://sandbox.plaid.com'  # Use 'https://development.plaid.com' or 'https://production.plaid.com' if applicable
PLAID_ENV = 'sandbox'  # Change to 'development' or 'production' when ready


if PLAID_ENV == 'sandbox':
    PLAID_HOST = 'https://sandbox.plaid.com'
elif PLAID_ENV == 'development':
    PLAID_HOST = 'https://development.plaid.com'
else:
    PLAID_HOST = 'https://production.plaid.com'



PASSWORD_RESET_TIMEOUT = 86400  # 1 day (you can adjust this value)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this directory exists and is correctly set up

# SendGrid settings 
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = config('SENDGRID_API_KEY')

# Additional SendGrid settings (optional)
SENDGRID_SANDBOX_MODE_IN_DEBUG = False  # Set to True if you want to test without sending emails
SENDGRID_ECHO_TO_STDOUT = True  # Print emails to the console while in DEBUG mode
DEFAULT_FROM_EMAIL = "pritzkervlad@gmail.com"




# DigitalOcean Spaces configuration
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# DIGITALOCEAN_SPACES_KEY = config('DIGITALOCEAN_SPACES_KEY')
# DIGITALOCEAN_SPACES_SECRET = config('DIGITALOCEAN_SPACES_SECRET')
DIGITALOCEAN_STORAGE_BUCKET_NAME = 'photopritzkerinance'
DIGITALOCEAN_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = DIGITALOCEAN_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = DIGITALOCEAN_ENDPOINT_URL
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
    'ACL': 'public-read'  # Ensure files are publicly readable by default

}

AWS_QUERYSTRING_AUTH = False
 
AWS_LOCATION = ''
AWS_DEFAULT_ACL = None
