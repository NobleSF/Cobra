from django.db import models
from django.utils import timezone


class Approvable(models.Model):
  approved_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    abstract = True

  @property
  def is_approved(self):
    return bool(self.approved_at)
  @is_approved.setter
  def is_approved(self, value):
    if value and not self.approved_at:
      self.approved_at = timezone.now()
    elif not value:
      self.approved_at = None
