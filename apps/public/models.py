from django.db import models

class Cart(models.Model):
  #from apps.admin.models import Currency

  email               = models.EmailField(blank=True, null=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address_name        = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  promotions          = models.ManyToManyField('Promotion')

  wepay_checkout_id   = models.BigIntegerField(null=True, blank=True)
  anou_checkout_id    = models.CharField(max_length=15, null=True, blank=True)
  checked_out         = models.BooleanField(default=False)#does not need to be a date

  #total_charge        = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_discount      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_paid          = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_refunded      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #currency            = models.ForeignKey(Currency, null=True, blank=True)

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

class Item(models.Model):
  from apps.seller.models import Product
  cart                = models.ForeignKey('Cart')
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
    from apps.seller.models import Photo
    return Photo.objects.filter(product_id=self.product.id)

  @property
  def photo(self):
    photos = self.photos
    try: return photos[0]
    except: return None

  def __unicode__(self):
    #return u'%d units of %s' % (self.quantity, self.product.name)
    return unicode(self.product.name)

class Promotion(models.Model):
  name                = models.CharField(max_length=50,  null=True, blank=True)
  #description         = models.CharField(max_length=200, null=True, blank=True)
  #code                = models.CharField(max_length=50,  null=True, blank=True)
  #automatic           = models.BooleanField(default=False) #auto apply to cart

  #valid_on            = models.DateTimeField(null=True, blank=True)
  #expires_on          = models.DateTimeField(null=True, blank=True)

  def __unicode__(self):
    return unicode(self.name)

class Order(models.Model):
  from apps.seller.models import Product, ShippingOption, Image

  cart                = models.ForeignKey('Cart', related_name='orders')

  #charges breakdown in local currency (eg. dirhams in Morocco)
  products_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=8, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  total_charge        = models.DecimalField(max_digits=8, decimal_places=2)

  shipping_option     = models.ForeignKey(ShippingOption, null=True, blank=True)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  tracking_number     = models.CharField(max_length=50, null=True, blank=True)

  seller_paid_amount  = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  seller_paid_receipt = models.ForeignKey(Image, blank=True, null=True)

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

  @property
  def tracking_url(self):
    if self.tracking_number:
      return "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1=" + self.tracking_number
    else: return False

class Rating(models.Model):
  from apps.seller.models import Product
  from apps.admin.models import RatingSubject

  session_key         = models.CharField(max_length=32)
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return unicode(self.value)

class Ranking(models.Model):
  from apps.seller.models import Product

  product       = models.OneToOneField(Product)

  photography   = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  price         = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  appeal        = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')

  new_product   = models.DecimalField(max_digits=3, decimal_places=2)
  new_store     = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')

  #update history
  updated_at    = models.DateTimeField(auto_now = True)

  @property
  def subjects(self):
    return {'photography':  self.photography,
            'price':        self.price,
            'appeal':       self.appeal,
            'new_product':  self.new_product,
            'new_store':    self.new_store
           }

  @property
  def weighted_average(self):
    from apps.public.controller.product_ranking import WEIGHTS
    avg  = 0.0
    avg += float(self.photography * WEIGHTS['photography'])
    avg += float(self.price       * WEIGHTS['price'])
    avg += float(self.appeal      * WEIGHTS['appeal'])
    avg += float(self.new_product * WEIGHTS['new_product'])
    avg += float(self.new_store   * WEIGHTS['new_store'])
    return int(100 * avg / sum(WEIGHTS.values()))

  @property
  def weights_sum(self):
    from apps.public.controller.product_ranking import WEIGHTS
    sum = 0
    for key in WEIGHTS:
      sum += WEIGHTS[key]
    return sum

#signal receivers are in here
from apps.public.controller import product_ranking
