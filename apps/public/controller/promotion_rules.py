from apps.communication.controller.email_class import Email
from settings.people import Tom

def discount_for_cart_promotion(cart, promotion):
  if promotion.name == "subscribe discount":
    return 0
