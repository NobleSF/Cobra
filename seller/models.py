from django.db import models
from admin.models import Account, Country, Currency, ShippingOption, Image, Colors

class Seller(models.Model):
  account = models.ForeignKey(Account)
  name = models.CharField(max_length=50)
  email = models.CharField(max_length=50, null=True, blank=True)
  phone = models.BigIntegerField(null=True, blank=True)
  bio = models.TextField(null=True, blank=True)
  country = models.ForeignKey(Country)
  currency = models.ForeignKey(Currency)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Product(models.Model):
  seller = models.ForeignKey('Seller')
  is_sold = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  #product description elements
  product_type = models.ForeignKey('ProductType')
  artisans = models.ManyToManyField('Artisan')
  tools = models.ManyToManyField('Tool')
  materials = models.ManyToManyField('Material')
  colors = models.ManyToManyField(Colors)
  width = models.IntegerField(null=True, blank=True)
  height = models.IntegerField(null=True, blank=True)
  length = models.IntegerField(null=True, blank=True)
  weight = models.IntegerField(null=True, blank=True)
  price = models.IntegerField(null=True, blank=True)
  shipping_options = models.ManyToManyField(ShippingOption)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.product_type.name + ' #' + str(self.pk) + ' by ' + self.seller.name

#Product Attributes

class ProductType(models.Model):
  seller = models.ForeignKey('Seller')
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  image = models.ForeignKey(Image)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Artisan(models.Model):
  seller = models.ForeignKey('Seller')
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  image = models.ForeignKey(Image)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Tool(models.Model):
  seller = models.ForeignKey('Seller')
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  image = models.ForeignKey(Image)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Material(models.Model):
  seller = models.ForeignKey('Seller')
  name = models.CharField(max_length=50)
  description = models.TextField(null=True, blank=True)
  image = models.ForeignKey(Image)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.name

class Photo(models.Model): #Photos are for product pictures only.
  product = models.ForeignKey('Product')
  order = models.IntegerField()
  file = models.CharField(max_length=100)
  #update history
  created_at = models.DateTimeField(auto_now_add = True)
  updated_at = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.file
