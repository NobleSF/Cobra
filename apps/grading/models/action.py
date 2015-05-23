from django.db import models
from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.grading.models.action_type import ActionType

class Action(models.Model):
  seller          = models.ForeignKey('seller.Seller', related_name='actions')
  action_type     = models.ForeignKey(ActionType)
  initial_points  = models.BigIntegerField()
  created_at      = models.DateTimeField(auto_now_add = True)
  voided_at       = models.DateTimeField(null=True)

  @property
  def type(self):
    return self.action_type.type
  @type.setter
  def type(self, value):
    self.action_type = ActionType.objects.get(type = value)

  @property
  def points(self):
    time_diff = timezone.now() - self.created_at
    time_since = time_diff.seconds + time_diff.days * 24 * 3600 # in seconds
    three_months = 90 * 24 * 3600 # in seconds
    if three_months > time_since:
      return int(float(self.initial_points) * (three_months - time_since) / three_months)
    else:
      return 0

  @property
  def is_void(self):
    return True if self.voided_at else False
  @is_void.setter
  def is_void(self, value):
    if value and not self.voided_at:
      self.voided_at = timezone.now()
    elif not value:
      self.voided_at = None
