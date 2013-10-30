from django.db import models
from apps.seller.models import Product, Seller


class Listing(models.Model):
  product         = models.OneToOneField(Product, related_name='ebay_listing')
