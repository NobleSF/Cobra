from django.db import models

class Account(models.Model):
  username      = models.CharField(max_length=50, unique=True)
  password      = models.CharField(max_length=100)
  name          = models.CharField(max_length=50, blank=True, null=True)
  email         = models.EmailField(blank=True, null=True)
  phone         = models.CharField(max_length=15, blank=True, null=True)
  is_admin      = models.BooleanField(default=False)
                  # we will have to expand for different levels of admin
                  # as well as country specific admin
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.username

class Country(models.Model): #could expand on pypi.python.org/pypi/django-countries
  name          = models.CharField(max_length=100)
  code          = models.CharField(max_length=3)
  calling_code  = models.IntegerField()
  # assuming countries stick to one currency nationwide
  currency      = models.ForeignKey('Currency')

  def __unicode__(self):
    return self.code

class Currency(models.Model):
  name          = models.CharField(max_length=50)
  code          = models.CharField(max_length=3)
  exchange_rate_to_USD = models.FloatField()
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.code

class Color(models.Model):
  name          = models.CharField(max_length=15)

  def __unicode__(self):
    return self.name

class ShippingOption(models.Model):
  name          = models.CharField(max_length=50)
  country       = models.ForeignKey('Country')
  cost_formula  = models.CharField(max_length=50) #l,w,h(cm), g=weight(grams)
  image         = models.ForeignKey('Image')

  def __unicode__(self):
    return self.name

class Image(models.Model): #Images are used for navigation, thumbnail size
  url           = models.URLField()
  #thumbnail file location
  #update history
  created_at    = models.DateTimeField(auto_now_add = True)
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.url

class Order(models.Model):
  from seller.models import Product
  account             = models.ForeignKey('Account')
  notes               = models.TextField(blank=True, null=True)
  #charges breakdown
  products_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=6, decimal_places=2)
  discount_charge     = models.DecimalField(max_digits=6, decimal_places=2)
  discount_reason     = models.TextField(blank=True, null=True)
  total_charge        = models.DecimalField(max_digits=6, decimal_places=2)
  receipt             = models.TextField(blank=True, null=True)
  #shipping info
  shipped_on          = models.DateField(blank=True, null=True)
  shipping_address    = models.TextField()
  shipping_option     = models.ForeignKey('ShippingOption')
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=6, decimal_places=2)
  received_on         = models.DateField(blank=True, null=True)
  #order items
  product             = models.ManyToManyField(Product)
  #Status
  is_seller_notified  = models.BooleanField(default=False)
  is_seller_confirmed = models.BooleanField(default=False)
  is_shipped          = models.BooleanField(default=False)
  is_arrived          = models.BooleanField(default=False)
  is_reviewed         = models.BooleanField(default=False)
  is_artisan_paid     = models.BooleanField(default=False)
  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)
