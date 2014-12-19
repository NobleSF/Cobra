from django.db import models
from django.utils import timezone
from apps.public.models.customer import Customer
from apps.seller.models.product import Product

class Commission(models.Model):
  base_product              = models.ForeignKey(Product, null=True, related_name="commissions")
  product                   = models.OneToOneField(Product, related_name='commission') #new product is created for each new custom order

  customer                  = models.ForeignKey(Customer, related_name='commissions')
  notes                     = models.TextField(null=True, blank=True)

  quantity                  = models.SmallIntegerField(default=1)
  length                    = models.IntegerField(null=True, blank=True)
  width                     = models.IntegerField(null=True, blank=True)
  estimated_price           = models.SmallIntegerField(null=True, blank=True)
  estimated_weight          = models.SmallIntegerField(null=True, blank=True)

  estimated_completion_date = models.DateTimeField(null=True, blank=True)

  #director_notified
  artisan_confirmed_at      = models.DateTimeField(null=True, blank=True)
  invoice_sent_at           = models.DateTimeField(null=True, blank=True)
  invoice_paid_at           = models.DateTimeField(null=True, blank=True)

  artisan_notified_at       = models.DateTimeField(null=True, blank=True)
  in_progress_at            = models.DateTimeField(null=True, blank=True)
  complete_at               = models.DateTimeField(null=True, blank=True)
  shipped_at                = models.DateTimeField(null=True, blank=True)
  canceled_at               = models.DateTimeField(null=True, blank=True)

  #update history
  created_at                = models.DateTimeField(auto_now_add = True)
  updated_at                = models.DateTimeField(auto_now = True)

  # MODEL PROPERTIES
  @property
  def artisan_confirmed(self):
    return True if self.artisan_confirmed_at <= timezone.now() else False
  @artisan_confirmed.setter
  def artisan_confirmed(self, value):
    if not self.artisan_confirmed:
      self.artisan_confirmed_at = timezone.now()

  @property
  def invoice_sent(self):
    return True if self.invoice_sent_at <= timezone.now() else False
  @invoice_sent.setter
  def invoice_sent(self, value):
    if not self.invoice_sent:
      self.invoice_sent_at = timezone.now()

  @property
  def invoice_paid(self):
    return True if self.invoice_paid_at <= timezone.now() else False
  @invoice_paid.setter
  def invoice_paid(self, value):
    if not self.invoice_paid:
      self.invoice_paid_at = timezone.now()

  @property
  def artisan_notified(self):
    return True if self.artisan_notified_at <= timezone.now() else False
  @artisan_notified.setter
  def artisan_notified(self, value):
    if not self.artisan_notified:
      self.artisan_notified_at = timezone.now()

  @property
  def in_progress(self):
    return True if self.in_progress_at <= timezone.now() else False
  @artisan_notified.setter
  def in_progress(self, value):
    if not self.artisan_notified:
      self.in_progress_at = timezone.now()

  @property
  def complete(self):
    return True if self.complete_at <= timezone.now() else False
  @complete.setter
  def complete(self, value):
    if not self.complete:
      self.complete_at = timezone.now()

  @property
  def shipped(self):
    return True if self.shipped_at <= timezone.now() else False
  @artisan_notified.setter
  def shipped(self, value):
    if not self.shipped:
      self.shipped_at = timezone.now()

  @property
  def canceled(self):
    return True if self.canceled_at <= timezone.now() else False
  @artisan_notified.setter
  def canceled(self, value):
    if not self.canceled:
      self.canceled_at = timezone.now()

  @property
  def display_price_estimate(self):

    old_volume = self.base_product.length * self.base_product.width * self.base_product.height
    shortest_side = min(self.base_product.length, self.base_product.width, self.base_product.height)
    new_volume = self.length * self.width * shortest_side
    ratio = float(new_volume)/old_volume

    artisan_price = self.base_product.price * ratio
    anou_fee = 0.25 * artisan_price
    weight = self.base_product.weight * ratio * self.quantity

    #bump estimate to next shipping price tier if close
    weight = (self.custom_product.weight * 1.05) + 100


    return int(round(self.display_price))

  @property
  def is_bulk(self):
    return True if self.quantity > 1 else False

  # MODEL FUNCTIONS
