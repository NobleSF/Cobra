from django.db import models
from apps.common.models import Country


class ShippingOption(models.Model):
  name            = models.CharField(max_length=50)
  country         = models.ForeignKey(Country) #todo: refactor to define destination country
  image           = models.ForeignKey('Image', null=True, blank=True, on_delete=models.SET_NULL)

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
  def __unicode__(self):
    return self.name
