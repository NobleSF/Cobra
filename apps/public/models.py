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
  anou_checkout_id    = models.CharField(max_length=15, null=True, blank=True)
  checked_out         = models.BooleanField(default=False)#does not need to be a date

  #todo: add discount code or note or something
  receipt             = models.TextField(blank=True, null=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  @property
  def checkout_id(self):
    if self.wepay_checkout_id:
      return self.wepay_checkout_id
    elif self.anou_checkout_id:
      return self.anou_checkout_id
    else:
      return False

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
    try: return photos[0]
    except: return None

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return self.product.name

class Order(models.Model):
  from apps.seller.models import Product, ShippingOption
  from apps.admin.models import Account

  cart                = models.ForeignKey('Cart')

  #charges breakdown in local currency (eg. dirhams in Morocco)
  products_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=8, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  discount_charge     = models.DecimalField(max_digits=8, decimal_places=2, default=0)
  discount_reason     = models.CharField(max_length=100, null=True, blank=True)
  total_charge        = models.DecimalField(max_digits=8, decimal_places=2)

  shipping_option     = models.ForeignKey(ShippingOption, null=True, blank=True)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  tracking_number     = models.CharField(max_length=50, null=True, blank=True)

  seller_paid_amount  = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)

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

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  #derivative attributes
  @property
  def seller(self): return self.products.all()[0].seller

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
  from django.contrib.sessions.models import Session
  from apps.seller.models import Product
  from apps.admin.models import Account, RatingSubject

  session_key         = models.CharField(max_length=32)
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return unicode(self.value)

class Subscription(models.Model):
  email               = models.CharField(max_length=100, unique=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  created_at          = models.DateTimeField(auto_now_add = True)

class Visitor(models.Model):#I don't think we need this
  #but south isn't handling the deletion of this model very well
  #it may have never created the relationship table visitor-session
  from django.contrib.sessions.models import Session
  sessions            = models.ManyToManyField(Session)
  carts               = models.ForeignKey('Cart', null=True, blank=True)
