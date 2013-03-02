from django.db import models

class Seller(models.Model):
  from admin.models import Account, Country, Currency
  account       = models.ForeignKey(Account)
  name          = models.CharField(max_length=50)
  email         = models.EmailField(null=True, blank=True)
  phone         = models.BigIntegerField(null=True, blank=True)
  bio           = models.TextField(null=True, blank=True)
  country       = models.ForeignKey(Country)
  currency      = models.ForeignKey(Currency)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Asset(models.Model):
  from admin.models import Category
  PRODUCT  = 1
  ARTISAN  = 2
  TOOL     = 3
  MATERIAL = 4
  ILK_CHOICES = (
    (PRODUCT,  'product'),
    (ARTISAN,  'artisan'),
    (TOOL,     'tool'),
    (MATERIAL, 'material'),
  )
  seller        = models.ForeignKey('Seller')
  ilk           = models.PositiveSmallIntegerField(choices=ILK_CHOICES)
  rank          = models.SmallIntegerField()
  name          = models.CharField(max_length=50)
  description   = models.TextField(null=True, blank=True)
  image         = models.ForeignKey('Image')
  category      = models.ManyToManyField(Category)
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

  def ilk(self):
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
  product       = models.ForeignKey('Product')
  rank          = models.SmallIntegerField()
  url           = models.URLField()
  thumbnail     = models.URLField()
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.thumbnail

class Image(models.Model): #Images are used for navigation, thumbnail size
  url           = models.URLField()
  #thumbnail file location
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.url
