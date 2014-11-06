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
SITE_ID = 1


#todo: remove this from repo
################## 3RD PARTY SERVICES ##################
#these should all be environment variables, ideally

#AMAZON WEB STORAGE S3, STATIC FILE HOSTING
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAISBCAIGR4FHXJKBQ'
AWS_SECRET_ACCESS_KEY = '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'
if PRODUCTION:
  AWS_STORAGE_BUCKET_NAME = 'anou'
elif DEMO:
  AWS_STORAGE_BUCKET_NAME = 'anou-demo'
else:
  AWS_STORAGE_BUCKET_NAME = 'anou-stage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

#CLOUDINARY IMAGE AND PHOTO HOSTING
if PRODUCTION or STAGE or DEMO:
  CLOUDINARY = {
    'cloud_name':     'hork5h8x1',
    'api_key':        '697913462329845',
    'api_secret':     '-dc1wU2_xyJmYaeJP1Yimn2-cuA',
    'format':         'jpg',
    'transformation': 't_original',
    'upload_url':     'http://api.cloudinary.com/v1_1/hork5h8x1/image/upload/',
    'download_url':   'http://res.cloudinary.com/hork5h8x1/image/upload/'
  }
else:
  CLOUDINARY = {
    'cloud_name':     'anou',
    'api_key':        '155257496663982',
    'api_secret':     'z78hCbzKQ26-6UQoE0FvmguCP9A',
    'format':         'jpg',
    'transformation': 't_original',
    'upload_url':     'http://api.cloudinary.com/v1_1/anou/image/upload/',
    'download_url':   'http://res.cloudinary.com/anou/image/upload/'
  }

#SENDGRID EMAIL BACKEND
EMAIL_HOST          = 'smtp.sendgrid.net'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True

if PRODUCTION:
  EMAIL_HOST_USER     = 'app15107937@heroku.com'
  EMAIL_HOST_PASSWORD = 'tmuipovc'
else:
  EMAIL_HOST_USER     = 'limetree'
  EMAIL_HOST_PASSWORD = 'H0hner765@'

#TELERIVET SMS GATEWAY
if PRODUCTION:
  TELERIVET = {
    'api_key':          'DF6UFT49DW643UQWDC436PC2K6LKWEDC',
    'project_id':       'PJb41b4e785d567945065e25271c8bd1dd',
    'phone_id':         'PNe5ceaab258b60afe79687a5620c5c265',
    'phone_number':     '212637637566',#2120623809088
    'status_url':       'http://www.theanou.com/communication/sms/status_confirmation',
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://www.theanou.com/communication/sms/incoming',
    'webhook_secret':   'NT9NAEQUAGWWGG4WQ7GQHP7WHXPNZR3P'
  }
elif DEMO:
  TELERIVET = {
    'api_key':          'H3P3UPFQ2CKMXLDLFX446FCPXMDK42CL',
    'project_id':       'PJ6ff0b172f5c2b56a',
    'phone_id':         'PN5b6a6b06369c5812',
    'phone_number':     '5551212',
    'status_url':       'http://anou-cobra-demo.herokuapp.com/communication/sms/status_confirmation',
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://anou-cobra-demo.herokuapp.com/communication/sms/incoming',
    'webhook_secret':   'QNCWR2444MRT6R2G74UDTMTA6QKM2TET'
  }
else:
  TELERIVET = {
    'api_key':          'DF6UFT49DW643UQWDC436PC2K6LKWEDC',
    'project_id':       'PJ7b2437d72ffb96a200f05f33318f7809',
    'phone_id':         'PNf04607c4af8e227a58457b059a9d583c',
    'phone_number':     '0665555555',
    'status_url':       'http://localcobra.pagekite.me/communication/sms/status_confirmation', #http://respondto.it/anou-sms-status
    'status_secret':    'JuiceIsWorthTheSqueeze',
    'webhook_url':      'http://localcobra.pagekite.me/communication/sms/incoming',
    'webhook_secret':   'QNCWR2444MRT6R2G74UDTMTA6QKM2TET'
  }
if STAGE:
  TELERIVET['status_url'] = 'http://anou-cobra-stage.herokuapp.com/communication/sms/status_confirmation'
  TELERIVET['webhook_url'] = 'http://anou-cobra-stage.herokuapp.com/communication/sms/incoming'
TELERIVET['past_numbers'] = ['212637637566','2120623809088','5551212','0665555555']

#WEPAY PAYMENT AND CHECKOUT PROCESSING
if PAYMENTS_PRODUCTION:
  WEPAY = {
    'client_id':      '114473',
    'client_secret':  '443ad32d57',
    'access_token':   'PRODUCTION_ed41e33671a46b6a3a93e6c6c6d45265fcb62a8f04998d232391bcd3e39749f9',
    'account_id':     '519238566',
    'redirect_uri':   'http://www.theanou.com/checkout/confirmation'
  }
else:
  WEPAY = {
    'client_id':      '137470',
    'client_secret':  '463bfe717b',
    'access_token':   'STAGE_3c234c249310a336d4999b8604b73a27ac5ec6e7255ac9a7ef3d0b6c2629079e',
    'account_id':     '854657449',
    'redirect_uri':   'http://localcobra.pagekite.me/checkout/confirmation'
  }
if STAGE:
  WEPAY['redirect_uri'] = 'http://anou-cobra-stage.herokuapp.com/checkout/confirmation'
if DEMO:
  WEPAY['redirect_uri'] = 'http://anou-cobra-demo.herokuapp.com/checkout/confirmation'

from memcacheify import memcacheify
CACHES = memcacheify()

RAVEN_CONFIG = {
  'dsn': 'https://f590888e182a4110b137b51e58352072:b4289579833c4f47950a36fd340746b3@app.getsentry.com/12262',
}
############## END 3RD PARTY SERVICES ##################



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
