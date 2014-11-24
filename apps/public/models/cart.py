from datetime import timedelta
from django.db import models
from django.utils import timezone
from apps.admin.utils.decorator import postpone
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.public.controller.promotion_rules import discount_for_cart_promotion
from apps.public.models.promotion import Promotion
from jsonfield import JSONField

class Cart(models.Model):
  email               = models.EmailField(blank=True, null=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address_name        = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  promotions          = models.ManyToManyField(Promotion)

  #todo delete
  wepay_checkout_id   = models.BigIntegerField(null=True, blank=True)
  anou_checkout_id    = models.CharField(max_length=15, null=True, blank=True)
  stripe_charge_id    = models.CharField(max_length=35, null=True, blank=True)
  checkout_data       = JSONField(null=True, blank=True)

  checked_out         = models.BooleanField(default=False)#does not need to be a date
  #todo delete

  receipt             = models.TextField(blank=True, null=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  # MODEL PROPERTIES
  @property
  def checkout_id(self): #todo delete
    if self.wepay_checkout_id:
      return self.wepay_checkout_id
    elif self.anou_checkout_id:
      return self.anou_checkout_id
    elif self.stripe_charge_id:
      return self.stripe_charge_id[3:]
    else:
      return False

  # @property
  # def checked_out(self):
  #   try:
  #     self.checkout.objects.count()
  #   except RelatedObjectDoesNotExist:
  #     return False
  #   else: return True

  @property
  def email_with_name(self):
    if self.name and self.email:
      return "%s <%s>" % (self.name, self.email)
    else:
      return self.email

  @property
  def shipping_address(self):
    address  = "%s\n" % (self.address_name or self.name or "")
    address += ("%s\n" % self.address1) if self.address1 else ""
    address += ("%s\n" % self.address2) if self.address2 else ""
    address += ("%s, " % self.city) if self.city else ""
    address += ("%s " % self.state) if self.state else ""
    address += self.postal_code if self.postal_code else ""
    address += ("\n%s" % self.country) if self.country else ""
    return address.upper()

  # MODEL FUNCTIONS
  def addPromotion(self, promotion):
    pass #self.promotions.add(promotion)

  # def discounts(self):
  #   discounts = {}
  #   for promotion in self.promotions:
  #     discounts[promotion.name] = discount_for_cart_promotion(self.cart, promotion)
  #   discounts['summary'] = sum(discounts.values())
  #   return discounts



#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete

@receiver(pre_save, sender=Cart)
def setFullCountryName(sender, instance, **kwargs):
  from settings.country_codes import country
  try:
    if len(instance.country) == 2:
      instance.country = country[instance.country]
  except: pass