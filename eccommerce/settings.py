"""
Django settings for eccommerce project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from decouple import config #219 manejo de libreria que permite el

# Build paths inside the project like this: BASE_DIR / 'subdir'.
#BASE_DIR = Path(__file__).resolve(strict=True).parent.parent  #223
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY') #219

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default= True)  #219... se manda el parametro para que el dato retornado esta en boolean

#ALLOWED_HOSTS = ['eccommerce-env.eba-shpyuktc.us-west-2.elasticbeanstalk.com','*'] #222 , colocacion del host provicional de aws
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'category',
    'accounts',
    'store',
    'carts',
    'contact_App',
    'orders',
    'admin_honeypot', #219 complementar con un migrate
    #'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',  #linea agregada por azure
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_session_timeout.middleware.SessionTimeoutMiddleware',  #220 linea que hace uso del timeout para la sesion pip install django-session-timeout
]
#configuracion del tiempo que pasara antes de cerrar sesion #220
SESSION_EXPIRE_SECONDS = 3600 #segundos
#interaccion del usuario
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

SESSION_TIMEOUT_REDIRECT = 'accounts/login' #redireccion del template despues del timeout

ROOT_URLCONF = 'eccommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'], #para que los templates se tomen en automatico
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links', #registro del context para el filtrado de las categorias, nombreapp, archivo y funcion
                'carts.context_processors.counter',
            ],
        },
    },
]

WSGI_APPLICATION = 'eccommerce.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account' #aplicacion y clase que manejara la estructura de usuarios

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', #parametros a cambiar por el uso de postgresql
        'NAME': "tiendaHardware5", #cambiar por el nombre de la base de datos, tener en cuenta el uso de mayusculas, postgresql las cambia a minusculas
        'USER': 'tripaseca',
        'PASSWORD': '', #os.getenv('BD_PASSWORD'),
        'HOST' : '',
        'PORT': '5432',
        #'OPTIONS':{'sslmode': 'require'},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'    #225
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS=[
    'eccommerce/static'  #se aplico el comando ...manage.py collectstatic
]

# AWS S3 Static Files Configuration    #225
'''AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static'
'''

'''STATICFILES_DIRS = [
    'eccommerce/static',
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

DEFAULT_FILE_STORAGE = 'eccommerce.media_storages.MediaStorage'
'''

MEDIA_URL ='/media/'
MEDIA_ROOT = BASE_DIR /'media'


from django.contrib.messages import constants as messages
MESSAGES_TAGS = {
    messages.ERROR: 'danger',
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#parametros para la configuracion del servicio de emails
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
#host
EMAIL_HOST=config('EMAIL_HOST') #"smtp.gmail.com" #parametros de correo gmail
#protocolo de segurida del servidos de correo
EMAIL_USE_TLS= config('EMAIL_USE_TLS', cast=bool, default= True) #True
EMAIL_PORT = config('EMAIL_PORT', cast=int)  #587
EMAIL_HOST_USER = config('EMAIL_HOST_USER') #"cuaginais17@gmail.com"
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') #"xjvzefdpgkqmdbit" 

'''EMAIL_HOST='smtp.gmail.com'
EMAIL_USE_TLS=True
EMAIL_PORT=587
EMAIL_HOST_USER='cuaginais17@gmail.com'
EMAIL_HOST_PASSWORD='xjvzefdpgkqmdbit' '''

#cargar el package en boobtrrap
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

import os
if 'WEBSITE_HOSTNAME' in os.environ: # Running on Azure
    from .azure import *
