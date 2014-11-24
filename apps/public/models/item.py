from django.db import models
from apps.public.models.cart import Cart
from apps.seller.models.product import Product

class Item(models.Model):
  cart                = models.ForeignKey(Cart, related_name='items')
  product             = models.ForeignKey(Product, related_name='items_in_carts')
  #quantity           = models.PositiveIntegerField(default=1)
  #price
  #shipping_cost
  #currency

  # MODEL PROPERTIES
  @property
  def order(self):
    return self.product.orders.filter(checkout=self.cart.checkout).first()

  @property
  def price(self):
    #if not self.price:
    #only return price for unsold products
    if not self.product.orders.filter(checkout=self.cart.checkout):
      return self.product.display_price

  @property
  def photos(self):
    return self.product.photos

  @property
  def photo(self):
    return self.product.photo

  # MODEL FUNCTIONS
  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return unicode(self.product.name)
