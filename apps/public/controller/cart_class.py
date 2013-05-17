# based on https://github.com/bmentges/django-cart

from apps.public import models
class Cart:
  def __init__(self, request):
    cart_id = request.session.get('cart_id')#if no cart id, returns None
    if cart_id:
      try:
        cart = models.Cart.objects.get(id=cart_id, checked_out=False)
      except Exception as e:
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
    result = 0
    for item in self.cart.item_set.all():
      result += 1 #* item.quantity
    return result

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
