# based on https://github.com/bmentges/django-cart
class Cart:
  def __init__(self, request):
    cart_id = request.session.get('cart_id')#if no cart id, returns None
    if cart_id:
      try:
        cart = models.Cart.objects.get(id=cart_id, checked_out=False)
      except models.Cart.DoesNotExist:
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
    except models.Item.DoesNotExist:
      item = models.Item()
      item.cart = self.cart
      item.product = product
      #item.quantity = quantity
      item.save()
    else: #ItemAlreadyExists
      #item.quantity = item.quantity + int(quantity)
      item.save()

  def remove(self, product):
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except models.Item.DoesNotExist:
      #raise ItemDoesNotExist
      pass #i don't care
    else:
      item.delete()

  def update(self, product): #, quantity
    try:
      item = models.Item.objects.get(
        cart=self.cart,
        product=product,
      )
    except models.Item.DoesNotExist:
      raise ItemDoesNotExist

  def count(self):
    result = 0
    for item in self.cart.item_set.all():
      result += 1 * item.quantity
    return result

  def summary(self):
    result = 0
    for item in self.cart.item_set.all():
      result += item.price
    return result

  def clear(self):
    for item in self.cart.item_set.all():
      item.delete()
