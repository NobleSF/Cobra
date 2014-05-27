from django.db import models

class Country(models.Model): #could expand on pypi.python.org/pypi/django-countries
  name          = models.CharField(max_length=100)
  code          = models.CharField(max_length=3)
  calling_code  = models.IntegerField()
  # assuming countries stick to one currency nationwide
  currency      = models.ForeignKey('Currency')
  """
  exchange_rate
  name_adjective
  """

  def __unicode__(self):
    return self.code
