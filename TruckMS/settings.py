"""
Django settings for TruckMS project.

Generated by 'django-admin startproject' using Django 5.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8c@bx7340(98by3$5ha3l9v_a-w6fhz)tfi%hff-j%tp7d3b+i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin', # Enable Django admin interface
    'django.contrib.auth', # Enable authentication system
    'django.contrib.contenttypes', # Enable content types framework
    'django.contrib.sessions', # Enable session framework
    'django.contrib.messages', # Enable messaging framework
    'django.contrib.staticfiles',# # Enable static files handling
    'fleetApp', # Custom app for fleet management
    'channels', ## Enable Django Channels for WebSocket support
     
]
#Configure channels as the ASGI Application for websocket handling
ASGI_APPLICATION = 'TruckMS.asgi.application'

# Configure channel layers for real-time communication
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer', # Use Redis as the channel layer backend
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)], # Connect to Redis server on localhost at port 6379
        },
    },
}
# Configure the custom user model for authentication/ Authentication settings
AUTH_USER_MODEL = 'fleetApp.User'  # Use custom User model from fleet app
LOGIN_URL = 'login'  # Redirect unauthenticated users to login page
LOGIN_REDIRECT_URL = 'home'  # Redirect after login to homepage
LOGOUT_REDIRECT_URL = 'login'  # Redirect after logout to login page

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TruckMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TruckMS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.mysql',   #django.db.backends.postgresql_psycopg2',
        'NAME': "Truckingdb",
        'USER': "root",
        'PASSWORD': "Kopilga@2025", #"H70v1gfb9mF90J5xTmWv",
        'HOST': 'localhost', #"containers-us-west-45.railway.app",
        'PORT':'3306', # "6608",
    }
}

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.Mysql',
   #     'NAME': BASE_DIR / 'db.sqlite3',
  #  }
#}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  
STATIC_ROOT = BASE_DIR/'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465  # Use port 465 for SSL/TLS
EMAIL_HOST_USER = 'admin@npcg2c.com'  # Replace with your Zoho Mail email address
EMAIL_HOST_PASSWORD = 'kaydiaan@2024**'  # Replace with your Zoho Mail email password
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'admin@npctender.com'  # Replace with your Zoho Mail email address

#STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
