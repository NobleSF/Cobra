from django.db import models
from datetime import datetime

class Cart(models.Model):
  email               = models.EmailField(blank=True, null=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  wepay_checkout_id   = models.BigIntegerField(null=True, blank=True)
  checked_out         = models.BooleanField(default=False)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  def discount(self):
    #for when we implement shipping groups and discounts
    return 0

  def total(self):
    sum = 0
    for item in self.items:
      sum += item.price
    return sum

class Item(models.Model):
  from apps.seller.models import Product

  cart                = models.ForeignKey('Cart')
  product             = models.ForeignKey(Product)
  #quantity           = models.PositiveIntegerField(default=1)

  @property
  def price(self):
    return self.product.display_price

  @property
  def photos(self):
    from apps.seller.models import Photo
    return Photo.objects.filter(product_id=self.product.id)

  @property
  def photo(self):
    photos = self.photos
    return photos[0]

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return self.product.name

class Order(models.Model):
  from apps.seller.models import Product, ShippingOption
  from apps.admin.models import Account

  cart                = models.ForeignKey('Cart')

  #charges breakdown in local currency (eg. dirhams in Morocco)
  products_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=6, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  discount_charge     = models.DecimalField(max_digits=6, decimal_places=2, default=0)
  discount_reason     = models.CharField(max_length=100, null=True, blank=True)
  total_charge        = models.DecimalField(max_digits=6, decimal_places=2)
  receipt             = models.TextField(blank=True, null=True)

  shipping_option     = models.ForeignKey(ShippingOption, null=True, blank=True)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=6, decimal_places=2)
  tracking_number     = models.CharField(max_length=50, null=True, blank=True)

  seller_paid_amount  = models.DecimalField(blank=True, null=True,
                                            max_digits=6, decimal_places=2)

  #order items
  products            = models.ManyToManyField(Product)

  #Status
  seller_notified_at  = models.DateTimeField(null=True, blank=True)
  seller_confirmed_at = models.DateTimeField(null=True, blank=True)
  shipped_at          = models.DateTimeField(null=True, blank=True)
  received_at         = models.DateTimeField(null=True, blank=True)
  reviewed_at         = models.DateTimeField(null=True, blank=True)
  seller_paid_at      = models.DateTimeField(null=True, blank=True)

  returned_at         = models.DateTimeField(null=True, blank=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  #derivative attributes
  @property
  def is_seller_notified(self): return True if self.seller_notified_at else False
  @property
  def is_seller_confirmed(self): return True if self.seller_confirmed_at else False
  @property
  def is_shipped(self): return True if self.shipped_at else False
  @property
  def is_received(self): return True if self.received_at else False
  @property
  def is_reviewed(self): return True if self.reviewed_at else False
  @property
  def is_seller_paid(self): return True if self.seller_paid_at else False

class Rating(models.Model):
  from apps.seller.models import Product
  from apps.admin.models import Account, RatingSubject
  #account             = models.ForeignKey(Account)
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return self.value

class Subscription(models.Model):
  email               = models.CharField(max_length=100, unique=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  created_at          = models.DateTimeField(auto_now_add = True)

class CustomerActivity(models.Model):
  from apps.seller.models import Product
  # ip address?
  # account_id?
  product_id          = models.ForeignKey(Product) # is this neccessary?
  action              = models.CharField(max_length=10) #what are the options?
  value               = models.IntegerField() #what's this for?
  created_at          = models.DateTimeField(auto_now_add = True)

class Visitor(models.Model):
  from django.contrib.sessions.models import Session

  sessions            = models.ManyToManyField(Session)
  carts               = models.ForeignKey('Cart', null=True, blank=True)
