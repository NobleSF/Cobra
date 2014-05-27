from django.db import models
from apps.seller.models.product import Product
from apps.seller.models.shipping_option import ShippingOption
from apps.seller.models.image import Image

class Item(models.Model):
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
    from apps.seller.models.photo import Photo
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

  notes               = models.TextField(blank=True, null=True)

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
  def is_complete(self): return True if self.seller_paid_at else False

  @property
  def tracking_url(self):
    tracking_url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1="
    return  tracking_url + self.tracking_number if self.tracking_number else False

class Rating(models.Model):
  from apps.admin.models import RatingSubject
  session_key         = models.CharField(max_length=32)
  #todo: tie to account
  product             = models.ForeignKey(Product)
  subject             = models.ForeignKey(RatingSubject)
  value               = models.SmallIntegerField()
  created_at          = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return unicode(self.value)

class Ranking(models.Model):
  from apps.seller.models.product import Product
  product       = models.OneToOneField(Product)
  photography   = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  price         = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  appeal        = models.DecimalField(max_digits=3, decimal_places=2, default='0.50')
  new_product   = models.DecimalField(max_digits=3, decimal_places=2, default='1.00')
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
    from apps.public.controllers.product_ranking import WEIGHTS
    avg  = 0.0
    avg += float(self.photography * WEIGHTS['photography'])
    avg += float(self.price       * WEIGHTS['price'])
    avg += float(self.appeal      * WEIGHTS['appeal'])
    avg += float(self.new_product * WEIGHTS['new_product'])
    avg += float(self.new_store   * WEIGHTS['new_store'])
    return int(100 * avg / sum(WEIGHTS.values()))

  @property
  def weights_sum(self):
    from apps.public.controllers.product_ranking import WEIGHTS
    sum = 0
    for key in WEIGHTS:
      sum += WEIGHTS[key]
    return sum

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(post_save, sender=Rating)
def updateRatingRankings(sender, instance, created, **kwargs):
  from apps.public.controllers.product_ranking import newProductResult, newStoreResult, photographyResult, priceResult, appealResult
  try:
    ranking, is_new = Ranking.objects.get_or_create(product = instance.product)
    if is_new:
      ranking.new_product = newProductResult(instance.product)
      ranking.new_store   = newStoreResult(instance.product)

    if instance.subject.name == 'Photography':
      ranking.photography = photographyResult(instance.product)
    elif instance.subject.name == 'Price':
      ranking.price = priceResult(instance.product)
    elif instance.subject.name == 'Appeal':
      ranking.appeal = appealResult(instance.product)
    ranking.save()
  except Exception as e:
    ExceptionHandler(e, "error on product_rankings.updateRatingRankings", sentry_only=True)
