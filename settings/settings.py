"""
Django settings for Cobra project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/

For checklist for production settings, see
See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

SECRET_KEY = 'sx^lszi^cgqdvv#g^djamr56=pkqatt(20=bjeo3++*v8rbue!'

ALLOWED_HOSTS = [
  '.theanou.com',
  '.herokuapp.com',
  'localhost'
]

#DEFINE THE ENVIRONMENT TYPE
PRODUCTION = STAGE = DEMO = LOCAL = False
if not os.environ.get('APP_NAME'):
  LOCAL = True
elif '-demo' == os.environ.get('APP_NAME')[-5:]:
  DEMO = True
elif '-stage' == os.environ.get('APP_NAME')[-6:]:
  STAGE = True
else:
  PRODUCTION = True

PAYMENTS_PRODUCTION = PRODUCTION
DEBUG = not (PRODUCTION or DEMO)
TEMPLATE_DEBUG = LOCAL

ADMINS = (('Developer', 'dev@theanou.com'),)
MANAGERS = ADMINS
ANOU_FEE_RATE = 0.10

# DATABASE
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
if PRODUCTION or STAGE or DEMO:
  DATABASES = {'default': dj_database_url.config()}
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
  from local_environment_settings import DATABASES

TIME_ZONE = 'Africa/Casablanca'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True #timezone awareness
SITE_ID = 1 #used by sitemap

#3RD PARTY SERVICES SETTINGS
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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

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
  'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
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
