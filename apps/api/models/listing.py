from django.db import models
from apps.seller.models.product import Product

class Listing(models.Model):
  product       = models.OneToOneField(Product, related_name='etsy_listing')
  product             = models.OneToOneField(Product, related_name='anou_listing')
  #slug                = models.CharField(max_length=100, null=True, blank=True)
  #title               = models.CharField(max_length=100, null=True, blank=True)
  #standard_title      = models.CharField(max_length=100, null=True, blank=True)
  #title_description   = models.CharField(max_length=300, null=True, blank=True)
  #description         = models.CharField(max_length=1000, null=True, blank=True)
  #price               = models.IntegerField(null=True, blank=True)
  #shipping_price      = models.IntegerField(null=True, blank=True)

  class Meta:
    app_label = 'api'

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
