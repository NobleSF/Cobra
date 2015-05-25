from django.utils import timezone
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.grading.models import ActionType, Action


class ActionMaker(object):
  def __init__(self, action_type=None, seller=None, product=None, order=None, rating=None):
    try:
      self.order = order or None
      self.rating = rating or None

      self.action = Action()

      if action_type != None:
        self.action.type = self.action_type = action_type
      if order:
        self.order = order
        product = self.order.product
      if product:
        self.action.product = self.product = product
        seller = self.product.seller
      if seller:
        self.action.seller = self.seller = seller

      elif rating:
        self.action.rating = self.rating = rating
        self.action.product = self.product = rating.product
        self.action.seller = self.seller = rating.product.seller
        if rating.subject.name == 'Photography':
          self.action.type = ActionType.PHOTOGRAPHY_RATING
        elif rating.subject.name == 'Price':
          self.action.type = ActionType.PRICE_RATING
        elif rating.subject.name == 'Appeal':
          self.action.type = ActionType.APPEAL_RATING

      self.action.initial_points = self.calculatePointsForAction()
      self.action.save()
    except Exception as e:
      ExceptionHandler(e, "in ActionMaker.__init__")


  def calculatePointsForAction(self):
    if not self.action.action_type.has_spread:
      points = self.action.action_type.max_points
      if self.action.action_type.is_penalty and points > 0:
        return int(points) * -1
      else:
        return int(points)

    else: #has spread
      #scale the point value between max and min
      min_points = self.action.action_type.min_points
      point_spread = self.action.action_type.max_points - self.action.action_type.min_points

      if self.action.action_type.type in [ActionType.ORDER_SMS,
                                     ActionType.SHIPPING_SMS]:
        #time between an order placed and the sms (just now)
        if self.action.action_type.type == ActionType.ORDER_SMS:
          spread_steps = [1, 12, 24, 36, 48]
        elif self.action.action_type.type == ActionType.SHIPPING_SMS:
          spread_steps = [24, 48, 72, 96]

        try:
          time_diff = timezone.now() - self.order.created_at
          hours = (time_diff.seconds / 3600) + (time_diff.days * 24)
          valid_steps = [step_value for step_value in spread_steps if hours <= step_value]
          if valid_steps:
            step = spread_steps.index(min(valid_steps))
          else:
            step = len(spread_steps) #value is past last limit = gets worst possible points

        except Exception as e:
          ExceptionHandler(e, "in ActionMaker.calculatePointsForAction A")

      if self.rating and self.action.action_type.type in [
                            ActionType.PHOTOGRAPHY_RATING,
                            ActionType.PRICE_RATING,
                            ActionType.APPEAL_RATING]:
        spread_steps = [5, 4, 3, 2] #1 is worst, because 1-5 rating is really 0-4
        try:

          if self.rating.value in spread_steps:
            step = spread_steps.index(self.rating.value)
          else:
            step = len(spread_steps)
          # a shortcut that produces same result:
          # step = rating.value - 1
          # spread_steps = range(4)
        except Exception as e:
          ExceptionHandler(e, "in ActionMaker.calculatePointsForAction B")

      if spread_steps and step:
        spread_length = len(spread_steps)
        position_fraction = (spread_length - step) / float(spread_length)
        points = self.action.action_type.min_points + (position_fraction * point_spread)
        return int(points)
