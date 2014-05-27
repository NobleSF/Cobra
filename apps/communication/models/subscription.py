from django.db import models

class Subscription(models.Model):
  email           = models.CharField(max_length=100, unique=True)
  name            = models.CharField(max_length=100, null=True, blank=True)
  created_at      = models.DateTimeField(auto_now_add = True)
