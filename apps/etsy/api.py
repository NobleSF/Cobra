import urllib,urllib2,json
from settings.settings import ETSY
from rauth import OAuth1Service as OAuth1
from rauth import OAuth2Service as OAuth2

class Etsy(object):
  """
  A client for the Etsy API.
  """

  def __init__(self, OAuth=False):
    self.requires_auth = OAuth
    #self.call_headers = {'Content-Type':  'application/json',
    #                     'User-Agent':    'Etsy Python SDK'}
    pass

  def queue(self, uri, method, paramters={}):
    #queue call requests for sending later
    pass

  def call(self, uri, method, parameters={}):

    url = ETSY['api_url'] + uri

    if method == "GET":
      parameters['api_key'] = ETSY['api_key']
      url += "?" + urllib.urlencode(parameters)
      success_code = 200

    elif method == "POST":
      success_code = 201


    elif method == "PUT":
      success_code = 200


    elif method == "DELETE":
      success_code = 200

    try:
      print "calling URL: %s" % url
      request = urllib2.Request(url)
      response = urllib2.urlopen(request, timeout=30)
      data = json.loads(response.read())
      response.close() #best practice

    except urllib2.URLError as e:
      print "request error" + str(e)
      return False

    else:
      if response.getcode() == success_code:
        print data
        return data

      elif response.getcode() in [400, 403, 500, 503]:
        messages = {'400': "Bad Request",
                    '403': "Forbidden",
                    '500': "Server Error",
                    '503': "Service Unavailable"}
        print messages[str(response.getcode())] + str(response.text)
        return False
      else:
        print "Unsuccessful, received response code "+str(response.getcode())
        return False

  def authorize(self):#, seller):

    request_token_url = ETSY['api_url'] + 'oauth/request_token'
    access_token_url  = ETSY['api_url'] + 'oauth/access_token'
    signin_url        = 'https://www.etsy.com/oauth/signin'

    permissions =  ['email_r',
                    'listings_r','listings_w','listings_d',
                    'transactions_r','transactions_w',
                    'billing_r',
                    'profile_r','profile_w',
                    'address_r','address_w',
                    'favorites_rw',
                    'shops_rw',
                    #'cart_rw',
                    'recommend_rw',
                    'feedback_r',
                    'treasury_r','treasury_w']
    parameters = {'scope': ' '.join(permissions)}
    request_token_url += "?scope=email_r"# + urllib.urlencode(parameters)

    auth = OAuth1(name='etsy',
                  consumer_key=ETSY['api_key'],
                  consumer_secret=ETSY['secret'],
                  request_token_url=request_token_url,
                  access_token_url=access_token_url)
                  #authorize_url='',
                  #base_url='')

    print request_token_url

    #request_token, request_token_secret =
    raw_request = auth.get_raw_request_token(params={
        #'oauth_callback': 'http://localcobra.pagekite.me/etsy/authorize',
        'oauth_token': None
      })

    return raw_request


  def image_upload(self, parameters = {}):
    pass
