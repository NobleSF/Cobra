from django.db import models

class Account(models.Model):
  username      = models.CharField(max_length=50, unique=True)
  password      = models.CharField(max_length=64)
  name          = models.CharField(max_length=50, blank=True, null=True)
  email         = models.EmailField(blank=True, null=True, unique=True)
  phone         = models.CharField(max_length=15, blank=True, null=True, unique=True)
  bank_name     = models.CharField(max_length=50, blank=True, null=True)
  bank_account  = models.CharField(max_length=100, blank=True, null=True)

  is_admin      = models.BooleanField(default=False, verbose_name='Admin')
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
  exchange_rate_to_USD = models.FloatField(verbose_name='Exchange Rate')
  updated_at    = models.DateTimeField(auto_now = True)

  def __unicode__(self):
    return self.code

class Color(models.Model):
  name          = models.CharField(max_length=15)
  hex_value     = models.CharField(max_length=6)

  def __unicode__(self):
    return self.name

class Category(models.Model):
  name          = models.CharField(max_length=50)
  #parent category?

  def __unicode__(self):
    return self.name

class RatingSubject(models.Model):
  #we may be able to move this to a list of choices for the Rating model
  name          = models.CharField(max_length=20)

  def __unicode__(self):
    return self.name
