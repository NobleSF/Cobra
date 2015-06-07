from django.db import models

class Color(models.Model):
  name          = models.CharField(max_length=15)
  hex_value     = models.CharField(max_length=6)

  class Meta:
    ordering = ['id']

  # MODEL PROPERTIES

  # MODEL FUNCTIONS
  def __unicode__(self):
    return self.name
