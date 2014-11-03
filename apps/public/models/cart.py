from django.db import models
from apps.public.models.promotion import Promotion

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

  wepay_checkout_id   = models.BigIntegerField(null=True, blank=True)
  anou_checkout_id    = models.CharField(max_length=15, null=True, blank=True)
  checked_out         = models.BooleanField(default=False)#does not need to be a date

  #total_charge        = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_discount      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_paid          = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #total_refunded      = models.DecimalField(max_digits=8, decimal_places=2,
  #                                          null=True, blank=True)
  #currency            = models.ForeignKey(Currency, null=True, blank=True)

  receipt             = models.TextField(blank=True, null=True)
  notes               = models.TextField(blank=True, null=True)

  #update history
  created_at          = models.DateTimeField(auto_now_add = True)
  updated_at          = models.DateTimeField(auto_now = True)

  class Meta:
    app_label = 'public'

  # MODEL PROPERTIES
  @property
  def checkout_id(self):
    if self.wepay_checkout_id:
      return self.wepay_checkout_id
    elif self.anou_checkout_id:
      return self.anou_checkout_id
    else:
      return False

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