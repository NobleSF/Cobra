from django.db import models
from apps.public.models.order import Order

class Email(models.Model):
  from_address    = models.EmailField()
  to_address      = models.EmailField()
  cc_address      = models.EmailField(null=True, blank=True)
  bcc_address     = models.EmailField(null=True, blank=True)
  subject         = models.CharField(max_length=200)
  html_body       = models.TextField(null=True, blank=True)
  text_body       = models.TextField(null=True, blank=True)
  attachment      = models.URLField(null=True, blank=True)
  order           = models.ForeignKey(Order, null=True, blank=True)

  created_at      = models.DateTimeField(auto_now_add = True)
