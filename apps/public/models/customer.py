from django.db import models
from jsonfield import JSONField
from apps.public.models.promotion import Promotion

class Customer(models.Model):
  email               = models.EmailField(blank=True, null=True)
  name                = models.CharField(max_length=100, null=True, blank=True)
  address_name        = models.CharField(max_length=100, null=True, blank=True)
  address1            = models.CharField(max_length=100, null=True, blank=True)
  address2            = models.CharField(max_length=100, null=True, blank=True)
  city                = models.CharField(max_length=50,  null=True, blank=True)
  state               = models.CharField(max_length=50,  null=True, blank=True)
  postal_code         = models.CharField(max_length=15,  null=True, blank=True)
  country             = models.CharField(max_length=50,  null=True, blank=True)

  # UPDATE HISTORY
  created_at          = models.DateTimeField(auto_now_add=True)
  updated_at          = models.DateTimeField(auto_now=True)

  # MODEL PROPERTIES
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

#SIGNALS AND SIGNAL REGISTRATION
from django.dispatch import receiver
from django.db.models.signals import pre_save

@receiver(pre_save, sender=Customer)
def setFullCountryName(sender, instance, **kwargs):
  from settings.country_codes import country
  try:
    if len(instance.country) == 2:
      instance.country = country[instance.country]
  except: pass