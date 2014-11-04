from django.db import models

class Promotion(models.Model):
  name                = models.CharField(max_length=50,  null=True, blank=True)
  #description         = models.CharField(max_length=200, null=True, blank=True)
  #code                = models.CharField(max_length=50,  null=True, blank=True)
  #automatic           = models.BooleanField(default=False) #auto apply to cart

  #valid_on            = models.DateTimeField(null=True, blank=True)
  #expires_on          = models.DateTimeField(null=True, blank=True)

  # MODEL PROPERTIES
  # MODEL FUNCTIONS
  def __unicode__(self):
    return unicode(self.name)