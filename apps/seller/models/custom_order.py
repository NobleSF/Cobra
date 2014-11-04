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

  # MODEL PROPERTIES
  # MODEL FUNCTIONS


  @property
  def display_price_estimate(self):

    old_volume = self.base_product.length * self.base_product.width * self.base_product.height
    new_volume = self.custom_product.length * self.custom_product.width * self.custom_product.height
    ratio = float(new_volume)/old_volume

    custom_product.price = base_product.price * ratio
    custom_product.weight = base_product.weight * ratio
    #bump estimate to next shipping price tier if close
    custom_product.weight = (custom_product.weight * 1.05) + 100
    custom_product.shipping_option.add(base_product.shipping_options.all()[0])

    return int(round(custom_product.display_price))
