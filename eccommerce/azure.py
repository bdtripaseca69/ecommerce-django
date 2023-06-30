from .settings import *
import os

from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []
CSRF_TRUSTED_ORIGINS = ['https://'+ os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': hostname,
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS':{'sslmode': 'require'},
    }
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enables whitenoise for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

STATIC_URL = 'static/'    #225
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_STORAGE= "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS=[
    'eccommerce/static'  #se aplico el comando ...manage.py collectstatic
]

MEDIA_URL ='/media/'
MEDIA_ROOT = BASE_DIR /'media'