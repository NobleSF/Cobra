from apps.grading.models import ActionType, Action


class ActionMaker(object):
  def __init__(self, seller):
    self.action = Action()
    self.action.seller = seller

  def saveActionForCreatedProduct(self, product):
    self.action.type = ActionType.ADD_PRODUCT
    self.action.initial_points = self.calculatePointsForAction()
    self.action.save()

  def saveActionForEditedProduct(self, product):
    self.action.type = ActionType.EDIT_PRODUCT
    self.action.initial_points = self.calculatePointsForAction()
    self.action.save()

  def saveActionForOrderSMS(self, sms):
    self.action.type = ActionType.ORDER_SMS
    self.action.initial_points = self.calculatePointsForAction(sms=sms, order=sms.order)
    self.action.save()

  def saveActionForShippingSMS(self, sms):
    self.action.type = ActionType.SHIPPING_SMS
    self.action.initial_points = self.calculatePointsForAction(sms=sms, order=sms.order)
    self.action.save()

  def calculatePointsForAction(self, **kwargs):

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
        #time between an order placed and the sms
        if self.action.action_type.type == ActionType.ORDER_SMS:
          spread_steps = [1, 12, 24, 36, 48]
        elif self.action.action_type.type == ActionType.SHIPPING_SMS:
          spread_steps = [24, 48, 72, 96]

        try:
          sms, order = kwargs.get('sms'), kwargs.get('order')
          time_diff = sms.created_at - order.created_at
          hours = (time_diff.seconds / 3600) + (time_diff.days * 24)
          valid_steps = [step_value for step_value in spread_steps if hours <= step_value]
          if valid_steps:
            step = spread_steps.index(min(valid_steps))
          else:
            step = len(spread_steps) #value is past last limit = gets worst possible points

        except Exception as e:
          ExceptionHandler(e, "in ActionMaker.calculatePointsForAction A")

      if self.action.action_type.type in [ActionType.PHOTOGRAPHY_RATING,
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
          ExceptionHandler(e, "in ActionMaker.calculatePointsForAction B")

      if spread_steps and step:
        spread_length = len(spread_steps)
        position_fraction = (spread_length - step) / float(spread_length)
        points = self.action.action_type.min_points + (position_fraction * point_spread)
        return int(points)
