from django.db import models
from apps.public.models.order import Order

class SMS(models.Model):
  from_number     = models.CharField(max_length=15)
  to_number       = models.CharField(max_length=15)
  order           = models.ForeignKey(Order, null=True, blank=True)
  message         = models.CharField(max_length=160)
  auto_reply      = models.CharField(max_length=160, null=True, blank=True)

  telerivet_id    = models.CharField(max_length=34)
  status          = models.CharField(max_length=15, null=True, blank=True)

  #update history
  created_at      = models.DateTimeField(auto_now_add = True)
  updated_at      = models.DateTimeField(auto_now = True)
