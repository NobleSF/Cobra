from django.db import models

class RatingSubject(models.Model):
  #we may be able to move this to a list of choices for the Rating model
  name          = models.CharField(max_length=20)

  def __unicode__(self):
    return self.name
