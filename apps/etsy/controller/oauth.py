import oauth2 as oauth
import urllib
from urlparse import parse_qsl
from settings.settings import ETSY

EtsyOAuthToken = oauth.Token

class EtsyOAuthClient(oauth.Client):
  def __init__(self, token=None):

    consumer = oauth.Consumer(ETSY['api_key'], ETSY['secret'])
    super(EtsyOAuthClient, self).__init__(consumer)

    self.request_token_url = ETSY['api_url'] + '/oauth/request_token'
    self.access_token_url  = ETSY['api_url'] + '/oauth/access_token'
    self.signin_url        = 'https://www.etsy.com/oauth/signin'
    self.token = token

  def get_request_token(self, **kwargs):
    permissions = ['email_r',
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
                  'treasury_r','treasury_w',]
    if 'scope' not in kwargs:
      kwargs['scope'] = ' '.join(permissions)

    request_token_url = '%s?%s' % (self.request_token_url, urllib.urlencode(kwargs))
    response, content = self.request(request_token_url, 'GET')
    return self._get_token(content)

  def get_signin_url(self, **kwargs):
    self.token = self.get_request_token(**kwargs)

    if self.token:
      return self.signin_url +'?'+ urllib.urlencode({'oauth_token': self.token.key})
    else:
      return None

  def get_access_token(self, oauth_verifier):
    self.token.set_verifier(oauth_verifier)
    response, content = self.request(self.access_token_url, 'GET')
    return self._get_token(content)

  def set_oauth_verifier(self, oauth_verifier):
    self.token = self.get_access_token(oauth_verifier)

  def do_oauth_request(self, uri, http_method, body="", headers={}):
    url = ETSY['api_url'] + uri

    if headers:
      response, content = self.request(url, http_method, body=body, headers=headers)
    else:
      response, content = self.request(url, http_method, body=body)

    #todo: log in sentry: 'do_oauth_request: content = %r' % content
    return (response, content)

  def _get_token(self, content):
    d = dict(parse_qsl(content))

    try:
      return oauth.Token(d['oauth_token'], d['oauth_token_secret'])
    except KeyError, e:
      print str(e)
      return None
