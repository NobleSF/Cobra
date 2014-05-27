from django.db import models


class Order(models.Model):
  cart                = models.ForeignKey('Cart', related_name='orders')

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

  #derivative attributes
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
