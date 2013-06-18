from django.db import models

class Email(models.Model):
  from_address    = models.EmailField()
  to_address      = models.EmailField()
  cc_address      = models.EmailField(null=True, blank=True)
  bcc_address     = models.EmailField(null=True, blank=True)
  subject         = models.CharField(max_length=200)
  html_body       = models.TextField(null=True, blank=True)
  text_body       = models.TextField(null=True, blank=True)
  attachment      = models.URLField(null=True, blank=True)
  created_at      = models.DateTimeField(auto_now_add = True)

class SMS(models.Model):
  from_number     = models.CharField(max_length=10)
  to_number       = models.CharField(max_length=10)
  message         = models.CharField(max_length=160)
  auto_reply      = models.CharField(max_length=160, null=True, blank=True)

  telerivet_id    = models.CharField(max_length=34)
  status          = models.CharField(max_length=15, null=True, blank=True)

  #update history
  created_at      = models.DateTimeField(auto_now_add = True)
  updated_at      = models.DateTimeField(auto_now = True)