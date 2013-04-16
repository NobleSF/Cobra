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
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Asset(models.Model):
  from admin.models import Category
  seller        = models.ForeignKey('Seller')
  ilk           = models.CharField(max_length=10)#product,artisan,tool,material
  name          = models.CharField(max_length=50, null=True, blank=True)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image', null=True, blank=True)
  category      = models.ManyToManyField(Category, null=True, blank=True)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

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
  asset         = models.ManyToManyField('Asset')
  color         = models.ManyToManyField(Color)
  width         = models.SmallIntegerField(null=True, blank=True)
  height        = models.SmallIntegerField(null=True, blank=True)
  length        = models.SmallIntegerField(null=True, blank=True)
  weight        = models.SmallIntegerField(null=True, blank=True)
  price         = models.SmallIntegerField(null=True, blank=True)
  shipping_option = models.ManyToManyField('ShippingOption')
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.product_type.name + ' #' + str(self.pk) + ' by ' + self.seller.name

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
  original      = models.ImageField(upload_to='images/originals', max_length=200)
  thumb         = models.ImageField(upload_to='images/thumbs', null=True, max_length=200)
  pinky         = models.ImageField(upload_to='images/pinkies', null=True, max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def original_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.original
  def thumb_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.thumb
  def pinky_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.pinky

class Image(models.Model): #Images are used for navigation, thumbnail size
  original      = models.ImageField(upload_to='images/originals', max_length=200)
  thumb         = models.ImageField(upload_to='images/thumbs', null=True, max_length=200)
  pinky         = models.ImageField(upload_to='images/pinkies', null=True, max_length=200)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def original_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.original
  def thumb_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.thumb
  def pinky_url(self):
    from anou.settings import MEDIA_URL
    return MEDIA_URL + self.pinky
