import urllib,urllib2,json
import requests
from settings.settings import ETSY
from apps.etsy.controller.oauth import EtsyOAuthClient as Auth
import oauth2 as oauth


class Etsy(object):
  """
  A client for the Etsy API.
  """
  def __init__(self, oauth_shop=None):
    #self.call_headers = {'Content-Type':  'application/json',
    #                     'User-Agent':    'Anou Etsy App'}
    if oauth_shop:
      self.requires_auth = True
      self.token = oauth.Token(oauth_shop.auth_token, oauth_shop.auth_token_secret)
      self.auth = Auth(self.token)

  def call(self, uri, method='GET', parameters={}):
    """
    Actually do the request, and raise exception if an error comes back.
    """

    if method is not "POST": #GET, PUT, DELETE
      parameters['api_key'] = ETSY['api_key']
      uri += "?%s" % urllib.urlencode(parameters) if parameters else ""

    else:
      pass #need to puth the api_key in parameters still?

    url = ETSY['api_url'] + uri
    print "calling %s at %s" % (method, uri)


    if self.requires_auth:
      (response, content) = self.auth.do_oauth_request(uri, method)
      print response
      print content
      #return content

    else:
      try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request, timeout=30)
        data = json.loads(response.read())
        response.close() #best practice

      except urllib2.URLError as e:
        print "request error" + str(e)
        return False

      else:
        if response.getcode() > 201:

          if response.getcode() in [400, 403, 500, 503]:
            messages = {400: "400:Bad Request",
                        403: "403:Forbidden",
                        500: "500:Server Error",
                        503: "503:Service Unavailable"}
            print "%d:%s >>> %s" % (response.getcode(),
                                    messages[response.getcode()],
                                    str(response.text))
          else:
            print "%d: Call Unsuccessful" % response.getcode()
          return False

        else:
          #print 'API returned %s response: %s' % (response.getcode(), response.text)
          #print data
          return data

  def queue(self, uri, method='GET', parameters={}, oauth=None):
    #queue call requests for sending later
    pass

  def image_upload(self, parameters = {}):
    pass
