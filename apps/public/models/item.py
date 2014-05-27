from django.db import models
from apps.seller.models.product import Product
from apps.seller.models.photo import Photo

from apps.public.models.cart import Cart

class Item(models.Model):
  cart                = models.ForeignKey(Cart)
  product             = models.ForeignKey(Product)
  #quantity           = models.PositiveIntegerField(default=1)

  @property
  def order(self):
    return self.product.order_set.get(cart=self.cart)

  @property
  def price(self):
    return self.product.display_price

  @property
  def photos(self):
    return Photo.objects.filter(product_id=self.product.id)

  @property
  def photo(self):
    photos = self.photos
    try: return photos[0]
    except: return None

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return unicode(self.product.name)
