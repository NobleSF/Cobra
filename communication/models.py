from django.db import models

class Email(models.Model):
  from_address    = models.EmailField()
  to_address      = models.EmailField()
  cc_address      = models.EmailField()
  bcc_address     = models.EmailField()
  subject         = models.CharField(max_length=200)
  message         = models.TextField()
  attachment      = models.URLField()
  created_at      = models.DateTimeField(auto_now_add = True)

class SMS(models.Model):
  from_number     = models.CharField(max_length=10)
  to_number       = models.CharField(max_length=10)
  message         = models.CharField(max_length=160)
  created_at      = models.DateTimeField(auto_now_add = True)
