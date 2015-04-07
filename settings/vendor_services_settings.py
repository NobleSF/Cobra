import os
from settings import PRODUCTION, STAGE, DEMO, LOCAL, PAYMENTS_PRODUCTION

if not LOCAL: #not PRODUCTION or STAGE or DEMO

  #AMAZON WEB STORAGE S3, STATIC FILE HOSTING
  AWS_ACCESS_KEY_ID       = os.environ.get('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY   = os.environ.get('AWS_SECRET_ACCESS_KEY')
  AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

  #CLOUDINARY IMAGE AND PHOTO HOSTING
  CLOUDINARY = {
    'cloud_name':     os.environ.get('CLOUDINARY_NAME'),
    'api_key':        os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret':     os.environ.get('CLOUDINARY_API_SECRET'),
    'cloudinary_url': os.environ.get('CLOUDINARY_API_SECRET'),
    'format': 'jpg',
    'transformation': 't_original'}
  CLOUDINARY['upload_url']      = "http://api.cloudinary.com/v1_1/%s/image/upload/" % CLOUDINARY['cloud_name']
  CLOUDINARY['download_url']    = "http://res.cloudinary.com/%s/image/upload/" % CLOUDINARY['cloud_name']

  #SENDGRID EMAIL BACKEND
  EMAIL_HOST          = 'smtp.sendgrid.net'
  EMAIL_PORT          = 587
  EMAIL_USE_TLS       = True
  EMAIL_HOST_USER     = os.environ.get('SENDGRID_USERNAME')
  EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')

  #TELERIVET SMS GATEWAY
  TELERIVET = {
    'api_key':          os.environ.get('TELERIVET_API_KEY'),
    'project_id':       os.environ.get('TELERIVET_PROJECT_ID'),
    'phone_id':         os.environ.get('TELERIVET_PHONE_ID'),
    'phone_number':     os.environ.get('TELERIVET_PHONE_NUMBER'),
    'status_url':       os.environ.get('TELERIVET_STATUS_URL'),
    'status_secret':    os.environ.get('TELERIVET_STATUS_SECRET'),
    'webhook_url':      os.environ.get('TELERIVET_WEBHOOK_URL'),
    'webhook_secret':   os.environ.get('TELERIVET_WEBHOOK_SECRET'),
  }
  #todo: relieve us of the need for this
  TELERIVET['past_numbers'] = ['212637637566','2120623809088','5551212','0665555555','212641534659']

  # PAYMENT PROCESSING BY STRIPE
  STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
  STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')

  #MEMCACHED CLOUD RESPONSE CACHEING
  CACHES = {
    'default': {
      'BACKEND': 'django_bmemcached.memcached.BMemcached',
      'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
      'OPTIONS': {
        'username': os.environ.get('MEMCACHEDCLOUD_USERNAME'),
        'password': os.environ.get('MEMCACHEDCLOUD_PASSWORD')
      }
    }
  }

  #EXCEPTION HANDLING AND REPORTING
  ROLLBAR = {
    'access_token': os.environ.get('ROLLBAR_ACCESS_TOKEN'),
    'environment': 'production' if PRODUCTION else 'development',
    'branch': 'master',
    'root': '/absolute/path/to/code/root',
  }

else: #local dev, use local file: settings/local_environment_settings.py
  try:
    from local_environment_settings import *
  except:
    print """----------------------------------
          No local environment settings found!
          Create file settings/local_environment_settings.py
          See settings/local_environment_settings_example.py for more information
          ----------------------------------"""
