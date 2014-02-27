from django.db import models
from apps.seller.models.product import Product

class CustomOrder(models.Model):
  base_product    = models.ForeignKey(Product, null=True,
                                      related_name="custom_orders")
  custom_product  = models.OneToOneField(Product)
  customer_name   = models.TextField(null=True, blank=True)
  customer_email  = models.TextField(null=True, blank=True)
  notes           = models.TextField(null=True, blank=True)
  estimated_completion_date = models.DateTimeField(null=True, blank=True)
  #update history
  created_at      = models.DateTimeField(auto_now_add = True)
  updated_at      = models.DateTimeField(auto_now = True)

  class Meta:
    app_label = 'seller'

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
