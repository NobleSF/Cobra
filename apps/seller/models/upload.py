from django.db import models

class Upload(models.Model): #images and photos before they exist
  public_id     = models.CharField(max_length=100, unique=True)
  created_at    = models.DateTimeField(auto_now_add = True)
  complete_at   = models.DateTimeField(null=True, blank=True)
  url           = models.URLField(max_length=200, null=True, blank=True)

  # MODEL PROPERTIES
  @property
  def is_complete(self): return True if self.complete_at else False

  # MODEL FUNCTIONS
