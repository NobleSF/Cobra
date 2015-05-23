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


def calculatePointsForAction(action, **kwargs):

  if not action.action_type.has_spread:
    points = action.action_type.max_points
    if action.action_type.is_penalty and points > 0:
      return int(points) * -1
    else:
      return int(points)

  else: #has spread
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
        sms = kwargs.get('sms')
        order = sms.order or kwargs.get('order')
        time_diff = sms.created_at - order.created_at
        hours = (time_diff.seconds / 3600) + (time_diff.days * 24)
        valid_steps = [step_value for step_value in spread_steps if hours <= step_value]
        if valid_steps:
          step = spread_steps.index(min(valid_steps))
        else:
          step = len(spread_steps) #value is past last limit = gets worst possible points

      except Exception as e:
        ExceptionHandler(e, "in action.calculatePointsForAction A")

    if action.action_type.type in [ActionType.PHOTOGRAPHY_RATING,
                                   ActionType.PRICE_RATING,
                                   ActionType.APPEAL_RATING]:
      spread_steps = [5, 4, 3, 2] #1 is worst, because 1-5 rating is really 0-4
      try:
        rating = kwargs.get('rating')
        if rating.value in spread_steps:
          step = spread_steps.index(rating.value)
        else:
          step = len(spread_steps)
        # a shortcut that produces same result:
        # step = rating.value - 1
        # spread_steps = range(4)
      except Exception as e:
        ExceptionHandler(e, "in action.calculatePointsForAction B")

    if spread_steps and step:
      spread_length = len(spread_steps)
      position_fraction = (spread_length - step) / float(spread_length)
      points = action.action_type.min_points + (position_fraction * point_spread)
      return int(points)
