DATABASES = {
  'default': {
    'ENGINE':   'django.db.backends.postgresql_psycopg2',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
    'NAME':     '',                                         # Or path to database file if using sqlite3.
    'USER':     '',                                         # Not used with sqlite3.
    'PASSWORD': '',                                         # Not used with sqlite3.
    'HOST':     'localhost',                                # Set to empty string for localhost. Not used with sqlite3.
    'PORT':     '5432',                                     # Set to empty string for default. Not used with sqlite3.
  }
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

#CLOUDINARY
CLOUDINARY = {
  'cloud_name':     '',
  'api_key':        '',
  'api_secret':     '',
  'cloudinary_url': '',
  'format':         'jpg',
  'transformation': '',
  'upload_url':     '',
  'download_url':   ''
}

#SENDGRID EMAIL BACKEND
# EMAIL_HOST          = 'smtp.sendgrid.net'
# EMAIL_PORT          = 587
# EMAIL_USE_TLS       = True
# EMAIL_HOST_USER     = ''
# EMAIL_HOST_PASSWORD = ''

#MAILCATCHER
EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

#TELERIVET SMS GATEWAY
TELERIVET = {
  'api_key':          '',
  'project_id':       '',
  'phone_id':         '',
  'phone_number':     '',
  'status_url':       '', #http://respondto.it
  'status_secret':    '',
  'webhook_url':      '',
  'webhook_secret':   ''
}
TELERIVET['past_numbers'] = []

STRIPE_SECRET_KEY = ""
STRIPE_PUBLIC_KEY = ""

#MEMCACHED CLOUD RESPONSE CACHEING
#no cacheing on local dev
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
  }
}

#EXCEPTION HANDLING AND REPORTING
ROLLBAR_ACCESS_TOKEN = ""
ROLLBAR = {
  'access_token': ROLLBAR_ACCESS_TOKEN,
  'environment': 'development',
  'branch': 'master',
  'root': '/absolute/path/to/code/root',
}
