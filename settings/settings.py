"""
Django settings for Cobra project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

For checklist for production settings, see
See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

SECRET_KEY = 'sx^lszi^cgqdvv#g^djamr56=pkqatt(20=bjeo3++*v8rbue!'

ALLOWED_HOSTS = [
  'www.theanou.com',
  'theanou.com',
  'anou-cobra.herokuapp.com',
  'anou-cobra-stage.herokuapp.com',
  'anou-cobra-demo.herokuapp.com',
  'localhost'
]

LOCAL_MACHINES = ['TOMCOUNSELL']
PRODUCTION = STAGE = DEMO = False

if 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra':
  PRODUCTION = True
elif 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra-stage':
  STAGE = True
elif 'NAME' in os.environ and os.environ['NAME'] == 'anou-cobra-demo':
  DEMO = True
else: #probably on LOCAL_MACHINES
  pass

PAYMENTS_PRODUCTION = PRODUCTION
DEBUG = not (PRODUCTION or DEMO)
TEMPLATE_DEBUG = not (STAGE or PRODUCTION or DEMO)

ADMINS = (('Developer', 'dev@theanou.com'),)
MANAGERS = ADMINS
ANOU_FEE_RATE = 0.10

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
if PRODUCTION or STAGE or DEMO:
  DATABASES = {'default': dj_database_url.config()}
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
  from local_environment_settings import DATABASES as local_databases
  DATABASES = local_databases

TIME_ZONE = 'Africa/Casablanca'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#todo: remove this from repo
from vendor_services_settings import *

if PRODUCTION or STAGE or DEMO:
  MEDIA_ROOT = '/media/'
else:
  MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

MEDIA_URL = 'http://s3.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME + '/'

STATIC_ROOT = '/static/'

AWS_STATIC_URL = 'http://s3.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME + '/'
STATIC_URL = AWS_STATIC_URL
if not (PRODUCTION or STAGE or DEMO): STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
  os.path.join(SITE_ROOT, 'static'),
  ('public', os.path.join(SITE_ROOT, 'apps/public/static')),
  ('seller', os.path.join(SITE_ROOT, 'apps/seller/static')),
  ('admin', os.path.join(SITE_ROOT, 'apps/admin/static')),
  ('communication', os.path.join(SITE_ROOT, 'apps/communication/static')),
)

MIDDLEWARE_CLASSES = (
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  #'django.contrib.auth.middleware.AuthenticationMiddleware',
  #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'settings.urls'
WSGI_APPLICATION = 'settings.wsgi.application'

TEMPLATE_DIRS = (
  os.path.join(SITE_ROOT, 'templates'),
  os.path.join(SITE_ROOT, 'templates/errors'),
)

INSTALLED_APPS = (
  'apps.public',
  'apps.seller',
  'apps.admin',
  'apps.communication',
  #'apps.api',
  'storages',
  #'django.contrib.admin',
  #'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.sites',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.sitemaps',
)
if PRODUCTION:
  INSTALLED_APPS += ('raven.contrib.django.raven_compat',) #Sentry

TEMPLATE_CONTEXT_PROCESSORS = (
  #'django.contrib.auth.context_processors.auth',
  'django.core.context_processors.debug',
  'django.core.context_processors.i18n',
  'django.core.context_processors.media',
  'django.core.context_processors.static',
  "django.core.context_processors.tz",
  'django.contrib.messages.context_processors.messages',
  'django.core.context_processors.request',
)

#Automated and Unit Testing
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
