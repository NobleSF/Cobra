from django.db import models
from seller.models import Product
from admin.models import Account

class CustomerActivity(models.Model):
  product_id = models.ForeignKey(Product)
  action = models.CharField(max_length=10)
  value = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add = True)

class Rating(models.Model):
  account = models.ForeignKey(Account)
  product_id = models.ForeignKey(Product)
  subject = models.ForeignKey('RatingSubject')
  value = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add = True)

class RatingSubject(models.Model):
  name = models.CharField(max_length=20)
