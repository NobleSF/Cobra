from django.db import models

class Currency(models.Model):
  name                  = models.CharField(max_length=50)
  code                  = models.CharField(max_length=3)
  exchange_rate_to_USD  = models.FloatField(verbose_name='Exchange Rate')
  updated_at            = models.DateTimeField(auto_now = True)

  # MODEL PROPERTIES

  # MODEL FUNCTIONS
  def __unicode__(self):
    return self.code
