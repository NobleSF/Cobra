from django.db import models

class Seller(models.Model):
  from admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account)
  name          = models.CharField(max_length=50)
  email         = models.EmailField(null=True, blank=True)
  phone         = models.BigIntegerField(null=True, blank=True)
  bio           = models.TextField(null=True, blank=True)
  country       = models.ForeignKey(Country, null=True, blank=True)
  currency      = models.ForeignKey(Currency, null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class ArtisanManager(models.Manager):
  def get_query_set(self):
    return super(ArtisanManager, self).get_query_set().filter(ilk='artisan')

class UtilityManager(models.Manager):
  def get_query_set(self):
    return super(UtilityManager, self).get_query_set().filter(ilk='tool') | super(UtilityManager, self).get_query_set().filter(ilk='material')

class Asset(models.Model):
  from admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True)
  categories    = models.ManyToManyField(Category, null=True, blank=True)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  #managers
  artisans      = ArtisanManager()
  utilities     = UtilityManager()

  def __unicode__(self):
    return unicode(self.name)

  def get_ilk(self):
    return self._get_ilk_display()

class Product(models.Model):
  from admin.models import Color
  seller        = models.ForeignKey('Seller')
  is_sold       = models.BooleanField(default=False)
  is_active     = models.BooleanField(default=False)
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

  def shipping_cost(self):
    return self.weight/3

  def display_price(self):
    import locale
    locale.setlocale( locale.LC_ALL, '' )
    from anou.settings import ANOU_FEE

    cost_amalgum_boobs_bomb = self.price
    cost_amalgum_boobs_bomb *= (1 + ANOU_FEE)
    cost_amalgum_boobs_bomb += calculateShipping(self)
    cost_amalgum_boobs_bomb /= self.seller.currency.exchange_rate_to_USD
    cost_amalgum_boobs_bomb  = "$"+str(int(round(cost_amalgum_boobs_bomb)))
    #locale.currency(round(cost_amalgum_boobs_bomb), grouping=True)
    return cost_amalgum_boobs_bomb

  def name(self):
    return self.assets.get(ilk='product')[0].name

  def __unicode__(self):
    return self.name() + ' by ' +self.seller.name

class ShippingOption(models.Model):
  from admin.models import Country
  name          = models.CharField(max_length=50)
  country       = models.ForeignKey(Country)
  cost_formula  = models.CharField(max_length=50) #l,w,h(cm), g=weight(grams)
  image         = models.ForeignKey('Image')

  def __unicode__(self):
    return self.name

class Photo(models.Model): #Photos are exclusively product pictures.
  from anou.settings import MEDIA_URL
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
