import urllib,urllib2,json
from apps.etsy import settings

class Etsy(object):
  """
  A client for the Etsy API.
  """

  def __init__(self, api_key=settings.api_key, secret=settings.secret, production=True):
    """
    """
    self.api_key = api_key
    self.secret = secret

    if production:
      self.api_url = "https://openapi.etsy.com/v2/"
    else: #sandbox
      self.api_url = "https://openapi.etsy.com/v2/"

    #self.call_headers = {'Content-Type':  'application/json',
    #                     'User-Agent':    'Etsy Python SDK'}

  def get_user(self, user_id):
    uri = "users/" + user_id

    url     = self.api_url + uri+ "?" + urllib.urlencode({'api_key':self.api_key})

    params  = json.dumps({'api_key':self.api_key})

    request = urllib2.Request(url)
    print url

    response = urllib2.urlopen(request, timeout=30).read()
    return json.loads(response)
