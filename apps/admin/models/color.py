from django.db import models

class Color(models.Model):
  name          = models.CharField(max_length=15)
  hex_value     = models.CharField(max_length=6)

  def __unicode__(self):
    return self.name

  class Meta:
    ordering = ['id']
