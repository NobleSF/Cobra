# based on https://github.com/bmentges/django-cart

from apps.public import models
class Cart:
  def __init__(self, request, checkout_id=None):
    cart_id = request.session.get('cart_id')#if no cart id, returns None

    #override session cart if valid checkout_id is provided
    if checkout_id:
      try:
        cart_id = models.Cart.objects.get(wepay_checkout_id=checkout_id).id
      except:
        pass

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
    except Exception as e:
      pass #i don't care
    else:
      item.delete()

  def update(self, product): #, quantity
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except Exception as e:
      pass

  def saveData(self, attribute, value):
    try:
      if attribute == 'email':
        self.cart.email = value
      elif attribute == 'name':
        self.cart.name = value
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
      else:
        raise TypeError('attribute ' + attribute + ' cannot be saved in cart')

    except Exception as e:
      raise Exception
    else:
      self.cart.save()

  def getData(self, attribute):
    try:
      if attribute == 'email':
        value = self.cart.email
      elif attribute == 'name':
        value = self.cart.name
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
      else:
        raise TypeError('attribute ' + attribute + ' not found in cart')

    except Exception as e:
      raise Exception
    else:
      return value

  def count(self):
    #result = 0
    #for item in self.cart.item_set.all():
    #  result += 1 * item.quantity
    return len(self.cart.item_set.all())

  def summary(self):
    result = 0
    for item in self.cart.item_set.all():
      result += item.product.display_price()
    return '%.2f' % result

  def clear(self):
    for item in self.cart.item_set.all():
      item.delete()

  def checkout(self):
    self.cart.checked_out = True
    self.cart.save()

  def getWePayCheckoutURI(self):
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PRODUCTION
    try:
      wepay = WePay(PRODUCTION, WEPAY['access_token'])

      if PRODUCTION:
        redirect_uri = "http://anou-cobra.herokuapp.com/checkout/confirmation"
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

  def getWePayCheckoutData(self, request):
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PRODUCTION
    try:
      wepay = WePay(PRODUCTION, WEPAY['access_token'])
      wepay_response = wepay.call('/checkout', {
        'checkout_id': self.cart.wepay_checkout_id
      })

      if wepay_response.get('shipping_address'):
        self.saveData('name', wepay_response.get('name'))
        self.saveData('address1', wepay_response['shipping_address'].get('address1'))
        self.saveData('address2', wepay_response['shipping_address'].get('address2'))
        self.saveData('city', wepay_response['shipping_address'].get('city'))
        if wepay_response['shipping_address'].get('state'): #US address
          self.saveData('state', wepay_response['shipping_address'].get('state'))
          self.saveData('postal_code', wepay_response['shipping_address'].get('zip'))
        else:
          self.saveData('state', wepay_response['shipping_address'].get('region'))
          self.saveData('postal_code', wepay_response['shipping_address'].get('postcode'))
        self.saveData('country', wepay_response['shipping_address'].get('country'))

      #checkout the cart
      if (not self.cart.checked_out) and wepay_response.get('gross'):
        if wepay_response.get('state') in ['authorized', 'reserved', 'captured']:
          try: del request.session['cart_id']
          except: pass
          self.checkout()

    except Exception as e:
      return "error: " + str(e)
    else:
      return wepay_response
