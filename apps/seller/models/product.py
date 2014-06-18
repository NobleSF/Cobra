from django.db import models
from apps.admin.models.color import Color
from apps.seller.models.asset import Asset
from apps.seller.models.seller import Seller
from apps.seller.models.shipping_option import ShippingOption
from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler

class Product(models.Model):
  seller        = models.ForeignKey(Seller, related_name='products')

  #product description elements
  assets        = models.ManyToManyField(Asset)
  colors        = models.ManyToManyField(Color)
  width         = models.SmallIntegerField(null=True, blank=True)
  height        = models.SmallIntegerField(null=True, blank=True)
  length        = models.SmallIntegerField(null=True, blank=True)
  weight        = models.SmallIntegerField(null=True, blank=True)
  price         = models.SmallIntegerField(null=True, blank=True)
  shipping_options = models.ManyToManyField(ShippingOption)

  #MIGRATE DATA TO API LISTING#
  active_at     = models.DateTimeField(null=True, blank=True) #seller add #todo:move to listing
  deactive_at   = models.DateTimeField(null=True, blank=True) #seller remove #todo:move to listing
  in_holding    = models.BooleanField(default=False) #held by admin #todo:move to listing
  approved_at   = models.DateTimeField(null=True, blank=True) #admin approval #todo:move to listing
  sold_at       = models.DateTimeField(null=True, blank=True)
  #MIGRATE DATA TO API LISTING#

  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  class Meta:
    ordering = ['-sold_at', '-id']
    app_label = 'seller'

  # MODEL PROPERTIES

  @property
  def photo(self):
    try:
      return self.photos.exclude(is_progress=True)[0]
    except:
      return None

  @property
  def name(self):
    try:
      if self.assets.filter(ilk='product')[0].name:
        return self.assets.filter(ilk='product')[0].name
      else:
        return str(self.id)
    except:
      return str(self.id)

  #@property
  #def artisan(self):
  #  try:
  #    return self.assets.filter(ilk='artisan')[0]
  #  except:
  #    return None

  @property
  def parent_category(self):
    try:
      return self.category if self.category.is_parent_category else self.category.parent_category
    except:
      return None

  @property
  def category(self):
    try:
      return self.assets.filter(ilk='product')[0].categories.all()[0]
    except:
      return None

  @property
  def rating(self):#overall rating
    from django.db.models import Avg
    #the rounded average of all ratings
    try: return int(round(self.rating_set.aggregate(average=Avg('value'))['average']))
    except: return ''

  @property
  def ratings(self):#rating by subject
    from django.db.models import Avg
    try:
      #get average rating by subject
      query = (self.rating_set.values('subject')
                  .annotate(average=Avg('value'))
                  .values('subject__name','average')
                 )
      #make dictionry: key, value = subject name, rounded rating
      ratings = {}
      for rating in query:
        ratings[rating['subject__name']] = int(round(rating['average']))
      return ratings
    except: return {}

  @property
  def is_complete(self):
    if (self.assets.filter(ilk='product').count() #has product type
        and self.assets.filter(ilk='artisan').count() #has artisan
        and self.photos.count() #has photo
        and self.shipping_options.count() #has shipping option
        and self.display_price #has price
        and self.weight #has weight
    ):
      return True
    else:
      return False

  @property
  def anou_fee(self):
    from settings.settings import ANOU_FEE_RATE
    if self.price:
      fee = self.price * ANOU_FEE_RATE / (1-ANOU_FEE_RATE)
      return int(round(fee)) #round off for local currencies
    else:
      return 0

  @property
  def shipping_cost(self):
    from apps.seller.controllers.shipping import calculateShippingCost
    if self.weight and len(self.shipping_options.all()) > 0:
      return calculateShippingCost(self.weight, self.shipping_options.all()[0], 'US')
    else:
      return 0

  @property
  def local_shipping_cost(self):
    from apps.seller.controllers.shipping import calculateShippingCost
    if self.weight and len(self.shipping_options.all()) > 0:
      return calculateShippingCost(self.weight, self.shipping_options.all()[0], 'MA')
    else:
      return 0

  @property
  def seller_paid_amount(self):
    if self.price:
      return self.price + self.shipping_cost
    else:
      return 0

  @property
  def intl_price(self):
    if self.price:
      return self.price + self.anou_fee + self.shipping_cost
    else:
      return 0

  @property
  def usd_price(self): #convert to USD
    if self.intl_price:
      local_currency = self.seller.country.currency
      return self.intl_price/float(local_currency.exchange_rate_to_USD)
    else:
      return 0

  @property
  def ebay_fee(self): #eBay + PayPal fee is $0.30 plus 12.9% of total
    if self.usd_price:
      fee = 0.30
      fee += (0.129/(1-0.129)) * (self.usd_price + fee)
      return fee
    else:
      return 0

  @property
  def ebay_price(self): #add fees and round to the nearest $1
    if self.usd_price:
      return int(round(self.usd_price + self.ebay_fee))
    else:
      return 0

  @property
  def etsy_fee(self): #Etsy + EtsyCheckout fee is $0.45 plus 6.5% of total
    if self.usd_price:
      fee = 0.40
      fee += (0.065/(1-0.065)) * (self.usd_price + fee)
      return fee
    else:
      return 0

  @property
  def etsy_price(self): #add fees and round to the nearest $1
    return int(round(self.usd_price + self.etsy_fee))


  # MODEL FUNCTIONS
  def belongsToPhone(self, phone_number):
    try:
      seller_phone = self.seller.account.phone
      return True if (phone_number[-8:] == seller_phone[-8:]) else False
    except Exception as e:
      ExceptionHandler(e, "in Product.belongsToPhone")
      return False

  def __unicode__(self):
    return unicode(self.name)


#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(pre_delete, sender=Product)
def onDelete(sender, instance, **kwargs):
  try:
    pass #todo: copy instance to reporting app
  except Exception as e:
    ExceptionHandler(e, "error on product.onDelete pre_delete signal")

@receiver(post_save, sender=Product)
def createRanking(sender, instance, created, update_fields, **kwargs):
  try:
    from apps.public.models.ranking import Ranking
    from apps.public.controllers.product_ranking import updateRankings, newProductResult
    if created:
      ranking, is_new = Ranking.objects.get_or_create(product = instance)
      ranking.new_product = newProductResult(instance)
  except Exception as e:
    ExceptionHandler(e, "error on product.createRanking post_save signal")
