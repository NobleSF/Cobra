from apps.public import models
from apps.admin.utils.exception_handling import ExceptionHandler
from django.utils import timezone
from datetime import timedelta
from apps.public.controller.promotion_rules import discount_for_cart_promotion

def cleanupCarts():
  from apps.seller.models.product import Product

  try:
    time_1_hour_ago = timezone.now() - timedelta(hours=1)
    recently_purchased_products = Product.objects.filter(sold_at__gte=time_1_hour_ago)

    #remove sold products from any carts that have not checked out yet
    for product in recently_purchased_products:
      if len(product.item_set.all()) > 1:
        for item in product.item_set.all():
          if not item.cart.checked_out:
            item.delete()

  except Exception as e:
    ExceptionHandler(e, "error on cart cleanup")

# based on https://github.com/bmentges/django-cart
class Cart(object):
  def __init__(self, request=None, checkout_id=None, cart_id=None):

    if request and not cart_id:
      cart_id = request.session.get('cart_id')#if no cart id, returns None

    #override session cart if valid checkout_id is provided
    if checkout_id:
      if isinstance(checkout_id, basestring) and checkout_id.startswith('MAN'):
        try: cart_id = models.Cart.objects.get(anou_checkout_id=checkout_id).id
        except: pass
      else:
        try: cart_id = models.Cart.objects.get(wepay_checkout_id=checkout_id).id
        except: pass

    if cart_id:
      try:
        cart = models.Cart.objects.get(id=cart_id)
      except:
        cart = self.new(request)
    else:
      cart = self.new(request)
    self.cart = cart

  def __iter__(self):
    for item in self.cart.item_set.all():
      yield item

  def new(self, request):
    cart = models.Cart()
    cart.save()
    request.session['cart_id'] = cart.id
    return cart

  def add(self, product): #, quantity=1
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except Exception as e:
      item = models.Item()
      item.cart = self.cart
      item.product = product
      #item.quantity = quantity
    else: #ItemAlreadyExists
      pass #item.quantity = item.quantity + int(quantity)
    finally:
      item.save()

  def remove(self, product):
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except Exception: pass #i don't care
    else:
      item.delete()

  def update(self, product): #, quantity
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except Exception: pass

  def saveData(self, attribute, value):
    try:
      if attribute == 'email':
        self.cart.email = value
      elif attribute == 'name':
        self.cart.name = value

      elif attribute == 'address_name':
        self.cart.address_name = value
      elif attribute == 'address1':
        self.cart.address1 = value
      elif attribute == 'address2':
        self.cart.address2 = value
      elif attribute == 'city':
        self.cart.city = value
      elif attribute == 'state':
        self.cart.state = value
      elif attribute == 'postal_code':
        self.cart.postal_code = value
      elif attribute == 'country':
        self.cart.country = value

      elif attribute == 'notes':
        self.cart.notes = value
      elif attribute == 'receipt':
        self.cart.receipt = value

      else:
        raise TypeError('attribute ' + attribute + ' cannot be saved in cart')

    except Exception as e:
      raise e
    else:
      self.cart.save()

  def getData(self, attribute):
    try:
      if attribute == 'email':
        value = self.cart.email
      elif attribute == 'name':
        value = self.cart.name

      elif attribute == 'address_name':
        value = self.cart.address_name
      elif attribute == 'address1':
        value = self.cart.address1
      elif attribute == 'address2':
        value = self.cart.address2
      elif attribute == 'city':
        value = self.cart.city
      elif attribute == 'state':
        value = self.cart.state
      elif attribute == 'postal_code':
        value = self.cart.postal_code
      elif attribute == 'country':
        value = self.cart.country

      elif attribute == 'notes':
        value = self.cart.notes
      elif attribute == 'receipt':
        value = self.cart.receipt

      else:
        raise TypeError('attribute ' + attribute + ' not found in cart')

    except Exception as e:
      raise e
    else:
      return value

  @property
  def checkout_id(self):
    if self.cart.wepay_checkout_id:
      return self.cart.wepay_checkout_id
    elif self.cart.anou_checkout_id:
      return self.cart.anou_checkout_id
    else:
      return False

  @property
  def contact(self):
    if self.cart.name and self.cart.email:
      return '%s (%s)' % (self.cart.name, self.cart.email)
    else:
      return False

  @property
  def shipping_address(self):
    if (self.cart.city and self.cart.country):
      return self.cart.shipping_address
    else:
      return False

  @property
  def notes(self):
    if self.cart.notes or self.cart.receipt:
      return True #todo: write html for notes and receipt combined
    else:
      return False

  def count(self):
    #result = 0
    #for item in self.cart.item_set.all():
    #  result += 1 * item.quantity
    return len(self.cart.item_set.all())

  def summary(self):
    result = 0
    for item in self.cart.item_set.all():
      result += item.product.display_price
    return '%.2f' % result

  def add_promotion(self, promotion):
    #self.cart.promotions.add(promotion)
    pass

  def discounts(self):
    discounts = {}
    for promotion in self.cart.promotions:
      discounts[promotion.name] = discount_for_cart_promotion(self.cart, promotion)
    discounts['summary'] = sum(discounts.values())
    return discounts

  def clear(self):
    for item in self.cart.item_set.all():
      item.delete()

  def checkout(self):
    if not self.cart.checked_out:
      self.cart.checked_out = True
      self.cart.save()

  def getAnouCheckoutId(self, type='manual'):
    from django.utils.dateformat import format

    try:
      if self.cart.anou_checkout_id:
        anou_checkout_id = self.cart.anou_checkout_id
      else:
        unix_timestamp = format(timezone.now(), u'U')
        if type == 'manual':
          anou_checkout_id = "MAN%s" % unix_timestamp
        #else 'ebay' or 'etsy'
        self.cart.anou_checkout_id = anou_checkout_id
        self.cart.wepay_checkout_id = None #shouldn't possibly have both
        self.cart.save()

    except Exception as e:
      return e
    else:
      return anou_checkout_id

  def getWePayCheckoutURI(self):
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PAYMENTS_PRODUCTION
    try:
      wepay = WePay(PAYMENTS_PRODUCTION, WEPAY['access_token'])

      if PAYMENTS_PRODUCTION:
        redirect_uri = "http://www.theanou.com/checkout/confirmation"
      else:
        redirect_uri = "http://localcobra.pagekite.me/checkout/confirmation"

      wepay_response = wepay.call('/checkout/create', {
        'account_id':         WEPAY['account_id'],
        'amount':             str(self.summary()),
        'short_description':  'Order Total',
        'type':               'GOODS',
        'mode':               'iframe',
        'fee_payer':          'payee',
        'redirect_uri':       redirect_uri,
        'require_shipping':   True
      })
      self.cart.wepay_checkout_id = wepay_response['checkout_id']
      self.cart.save()

    except Exception as e:
      return e
    else:
      return wepay_response['checkout_uri']

  def getWePayCheckoutData(self):
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PAYMENTS_PRODUCTION

    if not self.cart.wepay_checkout_id:
      return {}

    else:
      try:
        wepay = WePay(PAYMENTS_PRODUCTION, WEPAY['access_token'])
        wepay_response = wepay.call('/checkout', {
          'checkout_id': self.cart.wepay_checkout_id
        })
      except Exception as e:
        return {'error': e}
      else:
        return wepay_response

  def getCheckoutData(self):
    checkout_data = wepay_checkout_data = {}

    try:
      if str(self.cart.anou_checkout_id).startswith('MAN'):
        manual_checkout = True
      else:
        manual_checkout = False
        wepay_checkout_data = self.getWePayCheckoutData()

      checkout_data = wepay_checkout_data if wepay_checkout_data else {'manual_order':True}

      #name and email
      if self.cart.name:
        checkout_data['name'] = self.cart.name
      else:
        checkout_data['name'] = wepay_checkout_data.get('payer_name')
        self.cart.name = wepay_checkout_data.get('payer_name')
        self.cart.save()
      if self.cart.email:
        checkout_data['email'] = self.cart.email
      else:
        checkout_data['email'] = wepay_checkout_data.get('payer_email')
        self.cart.email = wepay_checkout_data.get('payer_email')
        self.cart.save()

      #shipping address
      if not checkout_data.get('shipping_address'):
        checkout_data['shipping_address'] = {} #create the dict

      if (not manual_checkout and
          not (self.cart.address1 and self.cart.city and
            self.cart.state and self.cart.postal_code)):
        #we do not have an address stored for this order
        #pull address from WePay and save it as our own

        #US or international address, all should match up except state, postal_code
        if wepay_checkout_data.get('shipping_address'):

          self.cart.address_name = wepay_checkout_data['shipping_address'].get('name')
          self.cart.address1  = wepay_checkout_data['shipping_address'].get('address1')
          self.cart.address2  = wepay_checkout_data['shipping_address'].get('address2')
          self.cart.city      = wepay_checkout_data['shipping_address'].get('city')
          if wepay_checkout_data['shipping_address'].get('country') == 'US':
            self.cart.country = 'USA'
          else:
            self.cart.country = wepay_checkout_data['shipping_address'].get('country')

          #check for non-US address first
          if (wepay_checkout_data['shipping_address'].get('region') or
              wepay_checkout_data['shipping_address'].get('post_code')):
           # international address, all should match except region -> state, post_code -> postal_code
           self.cart.state = wepay_checkout_data['shipping_address'].get('region')
           self.cart.postal_code = wepay_checkout_data['shipping_address'].get('post_code')

          else: #US address
            self.cart.state = wepay_checkout_data['shipping_address'].get('state')
            self.cart.postal_code = wepay_checkout_data['shipping_address'].get('zip')

        self.cart.save() #save all our address changes

      if self.cart.address_name:
        checkout_data['shipping_address']['name']       = self.cart.address_name
      checkout_data['shipping_address']['address1']     = self.cart.address1
      checkout_data['shipping_address']['address2']     = self.cart.address2
      checkout_data['shipping_address']['city']         = self.cart.city
      checkout_data['shipping_address']['state']        = self.cart.state
      checkout_data['shipping_address']['postal_code']  = self.cart.postal_code
      checkout_data['shipping_address']['country']      = self.cart.country

    except: pass

    return checkout_data
