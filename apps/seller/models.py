from django.db import models

class Seller(models.Model):
  from apps.admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account)
  name          = models.CharField(max_length=50)
  email         = models.EmailField(null=True, blank=True)
  phone         = models.BigIntegerField(null=True, blank=True)
  bio           = models.TextField(null=True, blank=True)
  city          = models.CharField(max_length=50, null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  coordinates   = models.CharField(max_length=30, null=True, blank=True)
  currency      = models.ForeignKey(Currency, null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Asset(models.Model):
  from apps.admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return unicode(self.name)

  def get_ilk(self):
    return self._get_ilk_display()

class Product(models.Model):
  from apps.admin.models import Color
  seller        = models.ForeignKey('Seller')
  is_sold       = models.BooleanField(default=False)
  is_active     = models.BooleanField(default=True) #for seller removal
  is_approved   = models.BooleanField(default=False) #for admin approval
  is_orderable  = models.BooleanField(default=False) #for custom orders

  #product description elements
  assets        = models.ManyToManyField('Asset')
  colors        = models.ManyToManyField(Color)
  width         = models.SmallIntegerField(null=True, blank=True)
  height        = models.SmallIntegerField(null=True, blank=True)
  length        = models.SmallIntegerField(null=True, blank=True)
  weight        = models.SmallIntegerField(null=True, blank=True)
  price         = models.SmallIntegerField(null=True, blank=True)
  shipping_options = models.ManyToManyField('ShippingOption')
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)


  def __unicode__(self):
    return self.name() + ' by ' +self.seller.name

  def name(self):
    if len(self.assets.filter(ilk='product')) > 0:
      if self.assets.filter(ilk='product')[0].name:
        return self.assets.filter(ilk='product')[0].name
    return str(self.id)

  def anou_fee(self):
    from settings.settings import ANOU_FEE_RATE
    if self.price:
      fee = self.price * ANOU_FEE_RATE
      return int(round(fee))
    else:
      return 0

  def shipping_cost(self):
    if self.weight:
      cost = 250 if self.weight > 200 else 50
      #need to pull in shipping cost formula for each in product.shipping_options

      return int(round(cost))
    else:
      return 0

  def local_price(self):
    if self.price:
      return self.price + self.anou_fee() + self.shipping_cost()
    else:
      return 0

  def display_price(self, locale='US'):
    cost_amalgum_boobs_bomb = self.local_price()
    #convert to USD and round to the nearest $1
    cost_amalgum_boobs_bomb /= self.seller.currency.exchange_rate_to_USD
    cost_amalgum_boobs_bomb = int(round(cost_amalgum_boobs_bomb))
    return cost_amalgum_boobs_bomb

  def is_complete(self):
    is_product = has_artisan = has_photo = has_price = False
    if len(self.assets.filter(ilk='product')) > 0:
      is_product = True
    if len(self.assets.filter(ilk='artisan')) > 0:
      has_artisan = True
    if len(self.photo_set.all()) > 0:
      has_photo = True
    if self.display_price:
      has_price = True

    if is_product and has_artisan and has_photo and has_price:
      return True
    else:
      return False

  def is_approved(self):
    if self.is_complete():
      return True
    else:
      return False

class ShippingOption(models.Model):
  from apps.admin.models import Country
  name          = models.CharField(max_length=50)
  country       = models.ForeignKey(Country)
  cost_formula  = models.CharField(max_length=50) #l,w,h(cm), g=weight(grams)
  image         = models.ForeignKey('Image')

  def __unicode__(self):
    return self.name

class Photo(models.Model): #Photos are exclusively product pictures.
  from settings.settings import MEDIA_URL
  product       = models.ForeignKey('Product')
  rank          = models.SmallIntegerField()
  original      = models.URLField(max_length=200)
  thumb         = models.URLField(null=True, max_length=200)
  pinky         = models.URLField(null=True, max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

class Image(models.Model): #Images are used for navigation, thumbnail size
  original      = models.URLField(max_length=200)
  thumb         = models.URLField(null=True, max_length=200)
  pinky         = models.URLField(null=True, max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)
