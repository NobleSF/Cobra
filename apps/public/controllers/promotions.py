from apps.admin.utils.exception_handling import ExceptionHandler

def discount_for_cart_promotion(cart, promotion):
  if promotion.name == "subscribe discount":
    return 0
