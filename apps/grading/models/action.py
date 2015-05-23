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


def calculatePointsForAction(action, **kwargs):

  if not action.action_type.has_spread:
    points = action.action_type.max_points
    return int(points) if not action.action_type.is_penalty else int(points) * -1
  else:
    #scale the point value between max and min
    min_points = action.action_type.min_points
    point_spread = action.action_type.max_points - action.action_type.min_points

    if action.action_type.type in [ActionType.ORDER_SMS,
                                   ActionType.SHIPPING_SMS]:
      #time between an order placed and the sms
      if action.action_type.type == ActionType.ORDER_SMS:
        spread_steps = [1, 12, 24, 36, 48]
      elif action.action_type.type == ActionType.SHIPPING_SMS:
        spread_steps = [24, 48, 72, 96]

      try:
        order, sms = kwargs.get('order'), kwargs.get('sms')
        time_diff = order.created_at - sms.created_at
        hours = (time_diff.seconds / 3600) + (time_diff.days * 24)
        value = hours

      except Exception as e:
        ExceptionHandler(e, "in action.calculatePointsForAction")

    if action.action_type.type in [ActionType.PHOTOGRAPHY_RATING,
                                   ActionType.PRICE_RATING,
                                   ActionType.APPEAL_RATING]:
      spread_steps = [1, 2, 3, 4, 5]
      try:
        rating = kwargs.get('rating')
        value = rating.value
      except Exception as e:
        ExceptionHandler(e, "in action.calculatePointsForAction")


    spread_length = len(spread_steps)
    step = spread_steps.index(min([s for s in spread_steps if s <= value]))
    position_fraction = spread_length - step / float(spread_length)
    points = action.action_type.min_points + (position_fraction * point_spread)
    return int(points)
