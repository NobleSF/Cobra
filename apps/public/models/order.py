from django.db import models
from apps.public.models.checkout import Checkout
from apps.seller.models.product import Product
from apps.seller.models.shipping_option import ShippingOption
from apps.seller.models.image import Image
from apps.public.models.cart import Cart

class Order(models.Model):
  cart                = models.ForeignKey(Cart, related_name='orders')
  checkout            = models.ForeignKey(Checkout, related_name='orders', null=True, blank=True)#todo remove null-true

  #charges breakdown in local currency (eg. dirhams in Morocco)
  products_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  anou_charge         = models.DecimalField(max_digits=8, decimal_places=2)
  shipping_charge     = models.DecimalField(max_digits=8, decimal_places=2)
  total_charge        = models.DecimalField(max_digits=8, decimal_places=2)

  shipping_option     = models.ForeignKey(ShippingOption, null=True, blank=True)
  #reported weight and cost after shipped
  shipping_weight     = models.FloatField(blank=True, null=True)
  shipping_cost       = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  tracking_number     = models.CharField(max_length=50, null=True, blank=True)

  seller_paid_amount  = models.DecimalField(blank=True, null=True,
                                            max_digits=8, decimal_places=2)
  seller_paid_receipt = models.ForeignKey(Image, blank=True, null=True)

  #order items
  products            = models.ManyToManyField(Product)
  product             = models.ForeignKey(Product, related_name='orders', null=True, blank=True)#todo remove null-true

  #Status
  seller_notified_at  = models.DateTimeField(null=True, blank=True)
  seller_confirmed_at = models.DateTimeField(null=True, blank=True)
  shipped_at          = models.DateTimeField(null=True, blank=True)
  received_at         = models.DateTimeField(null=True, blank=True)
  reviewed_at         = models.DateTimeField(null=True, blank=True)
  seller_paid_at      = models.DateTimeField(null=True, blank=True)
  returned_at         = models.DateTimeField(null=True, blank=True)

  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  # MODEL PROPERTIES
  @property
  def seller(self): return self.products.all()[0].seller

  @property
  def is_seller_notified(self): return True if self.seller_notified_at else False
  @property
  def is_seller_confirmed(self): return True if self.seller_confirmed_at else False
  @property
  def is_shipped(self): return True if self.shipped_at else False
  @property
  def is_received(self): return True if self.received_at else False
  @property
  def is_reviewed(self): return True if self.reviewed_at else False
  @property
  def is_seller_paid(self): return True if self.seller_paid_at else False
  @property
  def is_complete(self): return True if self.seller_paid_at else False

  @property
  def tracking_url(self):
    tracking_url = "https://tools.usps.com/go/TrackConfirmAction_input?qtc_tLabels1="
    return  tracking_url + self.tracking_number if self.tracking_number else False

  # MODEL FUNCTIONS


#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(post_save, sender=Order)
def createOrders(sender, instance, created, **kwargs):
  order = instance
  if created:
    from apps.communication.controller.order_events import communicateOrderCreated
    communicateOrderCreated(order)

