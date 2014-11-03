from django.db import models
from apps.admin.models.country import Country

class ShippingOption(models.Model):
  name            = models.CharField(max_length=50)
  country         = models.ForeignKey(Country)#todo: remove
  image           = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)

  class Meta:
    app_label = 'seller'

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
  def __unicode__(self):
    return self.name
