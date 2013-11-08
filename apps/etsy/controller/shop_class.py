from apps.etsy import models, api
from django.utils import timezone
from django.utils import simplejson as json

class Shop(object):

  def __init__(self, seller, etsy_shop_name=""):
    try:
      self.shop = models.Shop.objects.get(seller=seller)

    except models.Shop.DoesNotExist:
      self.shop = self.createFromSeller(seller, etsy_shop_name)

  def createFromSeller(self, seller, etsy_shop_name=""):
    #account creation not available in Etsy API
    #but we need to add the shop to our database

    #shop information
    shop_data = self.getEtsyShopData(etsy_shop_name)
    #user_data = self.getEtsyUserData(shop_data['login_name'])

    shop = models.Shop(seller     = seller,
                       user_id    = shop_data['user_id'],
                       login_name = shop_data['login_name'],
                       shop_id    = shop_data['shop_id'],
                       shop_name  = shop_data['shop_name'])
    shop.save()

    return shop

  def getAnouUserData(self):
    #format our own data defining what the etsy data should look like
    pass

  def getEtsyUserData(self, login_name=""):
    login_name = login_name if login_name else self.shop.login_name

    etsy = api.Etsy()
    user_method = "GET"
    uri = "/users/" + (login_name if login_name else str(self.shop.user_id))

    data = etsy.call(uri, method)
    if data['count'] == 1 and data['type'] == 'User':
      return data['results'][0]




  def updateUser(self):
    pass

  def getAnouShopData(self):
    #format our own data defining what the etsy data should look like
    pass

  def getEtsyShopData(self, shop_name=""):
    """
    https://www.etsy.com/developers/documentation/reference/shop#method_getshop
    """
    shop_name = shop_name if shop_name else self.shop.shop_name

    etsy = api.Etsy()
    method = "GET"
    uri = "/shops/%s" % (shop_name if shop_name else str(self.shop.shop_id))

    data = etsy.call(uri, method)
    if data['count'] == 1 and data['type'] == 'Shop':
      return data['results'][0]





  def updateShop(self):
    """
    https://www.etsy.com/developers/documentation/reference/shop#method_updateshop
    """
    method  = "PUT"
    uri     = '/shops/%s' % self.shop.shop_name
    etsy    = api.Etsy(self.shop)

    parameters = {
      'title':              self.shop.title or self.shop.default_title,
      'announcement':       self.shop.announcement,
      'sale_message':       self.shop.sale_message,
      'policy_welcome':     self.shop.policy_welcome,
      'policy_shipping':    self.shop.policy_shipping,
      'policy_refunds':     self.shop.policy_refunds,
      'policy_seller_info': self.shop.policy_seller_info,
      'policy_additional':  self.shop.policy_additional
    }

    ############## BEGIN MOVE LOGIC TO etsy.call ###############

    #from apps.etsy.controller.oauth import EtsyOAuthClient as Auth
    #import urllib
    #from settings.settings import ETSY
    #import oauth2 as oauth
    #
    #self.token = oauth.Token(self.shop.auth_token, self.shop.auth_token_secret)
    #auth = Auth(self.token)
    #
    #if parameters:
    #  uri += '?api_key=' + ETSY['api_key']
    #  uri += '&' + urllib.urlencode(parameters)
    #
    #print "calling %s at %s" % (method, uri)
    #
    #(response, content) = auth.do_oauth_request(uri, method)
    #print response
    #print content

    ################ END MOVED TO etsy.call ####################


    etsy.call(uri, method, parameters)
    #if all goes well?
      #return True








  def checkUser(self):
    #get user information
    etsy_user_data = getEtsyUserData()
    anou_user_data = getAnouUserData()

    #compare user_data to self.shop.seller data

    #all checks out?
    return True
    #else, return updateUser()

  def checkShop(self):
    #get shop information
    etsy_shop_data = getEtsyShopData()
    anou_shop_data = getAnouShopData()
    #compare shop_data to self.shop.seller data

    #all checks out?
    return True
    #else, return updateShop()

  def createShopSection(self):pass
  def getShopSection(self):pass
  def updateShopSection(self):pass
  def deleteShopSection(self):pass

  def uploadShopBanner(self):
    """
    https://www.etsy.com/developers/documentation/reference/shop#method_uploadshopbanner
    """
    method  = "POST"
    uri     = "shops/%d/appearance/banner" % self.shop.shop_id
    #image file




  def checkPermissions(self):
    """
    https://www.etsy.com/developers/documentation/getting_started/oauth#section_checking_permission_scopes_after_authentication
    """
    from apps.etsy.controller.oauth import EtsyOAuthClient as OAuth
    import urllib
    import oauth2 as oauth


    from settings.settings import ETSY

    etsy = api.Etsy()
    method = "GET"
    uri = '/oauth/scopes'
    uri += '?api_key=' + ETSY['api_key']

    self.token = oauth.Token(self.shop.auth_token, self.shop.auth_token_secret)
    auth = OAuth(self.token)

    print "calling %s at %s" % (method, uri)
    (response, content) = auth.do_oauth_request(uri, method)
    print content
