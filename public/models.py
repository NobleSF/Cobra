from django.db import models

class CustomerActivity(models.Model):
  from seller.models import Product
  # ip address?
  # account_id?
  product_id  = models.ForeignKey(Product) # is this neccessary?
  action      = models.CharField(max_length=10) #what are the options?
  value       = models.IntegerField() #what's this for?
  created_at  = models.DateTimeField(auto_now_add = True)

class Rating(models.Model):
  from seller.models import Product
  from admin.models import Account
  account     = models.ForeignKey(Account)
  product_id  = models.ForeignKey(Product)
  subject     = models.ForeignKey('RatingSubject')
  value       = models.SmallIntegerField()
  created_at  = models.DateTimeField(auto_now_add = True)

  def __unicode__(self):
    return self.value

class RatingSubject(models.Model):
  #we may be able to move this to a list of choices for the Rating model
  name        = models.CharField(max_length=20)

  def __unicode__(self):
    return self.name
