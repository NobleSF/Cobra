from django.db import models
from django.utils import timezone
from apps.public.models.customer import Customer
from apps.seller.models.product import Product

class Commission(models.Model):
  base_product              = models.ForeignKey(Product, null=True, related_name='commissions')
  # new product is created for each new custom order
  product                   = models.OneToOneField(Product, null=True, related_name='commission')

  customer                  = models.ForeignKey(Customer, null=True, related_name='commissions')
  notes                     = models.TextField(null=True, blank=True)

  quantity                  = models.SmallIntegerField(default=1)
  length                    = models.IntegerField(null=True, blank=True)
  width                     = models.IntegerField(null=True, blank=True)
  estimated_display_price   = models.SmallIntegerField(null=True, blank=True)
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
  def is_bulk(self):
    return True if self.quantity > 1 else False

  @property
  def public_id(self): return "C%d" % self.id

  # MODEL FUNCTIONS
  def createPriceEstimate(self, save=True):
    self.product = self.createProduct(False)
    if save:
      self.estimated_display_price = self.product.display_price
      self.save()
    return self.product.display_price

  def createWeightEstimate(self, save=True):
    self.product = self.createProduct(False)
    if save:
      self.estimated_weight = self.product.weight
      self.save()
    return self.product.weight

  def createProduct(self, save=True):
    self.product = Product(seller=self.base_product.seller) if not self.product else self.product

    self.base_product.sortDimensions() #sorts base_product dimensions and all set to positive integers
    base_size = self.base_product.length * self.base_product.width
    self.product.length = self.length or self.base_product.length
    self.product.width = self.width or self.base_product.width
    self.product.height = self.base_product.height

    new_size = self.product.length * self.product.width
    ratio = float(new_size) / base_size

    self.product.weight = int(((self.base_product.weight * ratio * 1.05) + 100) * self.quantity)
    self.product.price = int(self.base_product.price * ratio * self.quantity)

    if save:
      self.product.save()
      self.save()

    return self.product

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save

@receiver(pre_save, sender=Commission)
def createRelatedObjects(sender, instance, **kwargs):
  if not instance.product:
    instance.product = Product.objects.create(seller=instance.base_product.seller)
  instance.product.save()
  if instance.estimated_display_price and not instance.customer:
    instance.customer = Customer.objects.create()