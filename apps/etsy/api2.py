import urllib,urllib2,json
from settings.settings import ETSY
from urlparse import unquote, parse_qs
import json
import requests
from oauth_hook import OAuthHook

class Etsy(object):

  def __init__(self, oauth_token=None, oauth_token_secret=None, sandbox=False):
    self.url_base = ETSY['api_url']
    self.params = {'api_key': ETSY['api_key']}
    self.consumer_key = ETSY['api_key']
    self.consumer_secret = ETSY['secret']

    # generic authenticated oauth hook
    self.simple_oauth = OAuthHook(consumer_key=self.consumer_key,
                                  consumer_secret=self.consumer_secret)

    if oauth_token and oauth_token_secret:
      # full oauth hook for an authenticated user
      self.full_oauth = OAuthHook(oauth_token,
                                  oauth_token_secret,
                                  self.consumer_key,
                                  self.consumer_secret)

  def get_auth_url(self, permissions=[]):
      """
      Returns a url that a user is redirected to in order to authenticate with
      the etsy API. This is step one in the authentication process.
      oauth_token and oauth_token_secret need to be saved for step two.
      """
      endpoint = '/oauth/request_token'
      self.params = {}
      if permissions:
          self.params = {'scope': " ".join(permissions)}
      response = self.execute(endpoint, oauth=self.simple_oauth)
      parsed = parse_qs(response.text)
      url = parsed['login_url'][0]
      token = parsed['oauth_token'][0]
      secret = parsed['oauth_token_secret'][0]
      return {'oauth_token': token, 'url': url, 'oauth_token_secret': secret}

  def get_auth_token(self, verifier, oauth_token, oauth_token_secret):
      """
      Step two in the authentication process. oauth_token and oauth_token_secret
      are the same that came from the get_auth_url function call. Returned is
      the permanent oauth_token and oauth_token_secret that will be used in
      every subsiquent api request that requires authentication.
      """
      endpoint = '/oauth/access_token'
      self.params = {'oauth_verifier': verifier}
      oauth = OAuthHook(oauth_token, oauth_token_secret, self.consumer_key, self.consumer_secret)
      response = self.execute(endpoint, method='post', oauth=oauth)
      parsed = parse_qs(response.text)
      return {'oauth_token': parsed['oauth_token'][0], 'oauth_token_secret': parsed['oauth_token_secret'][0]}


  def execute(self, endpoint, method='get', oauth=None):
      """
      Actually do the request, and raise exception if an error comes back.
      """
      querystring = urllib.urlencode(self.params)
      url = "%s%s" % (self.url_base, endpoint)
      if querystring:
        url = "%s?%s" % (url, querystring)

      hooks = {}
      if oauth:
        # making an authenticated request, add the oauth hook to the request
        hooks = {'hooks': {'pre_request': oauth}}

      response = getattr(requests, method)(url, **hooks)

      if response.status_code > 201:
        e = response.text
        code = response.status_code
        print 'API returned %s response: %s' % (code, e)
      return response
