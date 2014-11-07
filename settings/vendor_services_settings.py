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
  else: #STAGE OR DEMO
    WEPAY = {
      'client_id':      '137470',
      'client_secret':  '463bfe717b',
      'access_token':   'STAGE_3c234c249310a336d4999b8604b73a27ac5ec6e7255ac9a7ef3d0b6c2629079e',
      'account_id':     '854657449',
    }
  if STAGE:
    WEPAY['redirect_uri'] = 'http://anou-cobra-stage.herokuapp.com/checkout/confirmation'
  if DEMO:
    WEPAY['redirect_uri'] = 'http://anou-cobra-demo.herokuapp.com/checkout/confirmation'

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

  #SENTRY EXCEPTION REPORTING
  RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN')
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
