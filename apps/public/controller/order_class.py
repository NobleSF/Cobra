from apps.public import models
from apps.admin.utils.exception_handling import ExceptionHandler
from apps.communication.controller import order_events
from django.utils import timezone

def getOrders(checkout_id):
  try:
    if "MAN" in str(checkout_id):
      cart = models.Cart.objects.get(anou_checkout_id = checkout_id)
    else:
      cart = models.Cart.objects.get(wepay_checkout_id = checkout_id)

    orders = cart.orders.all()
    if not orders:
      orders = createFromCart(cart)
      #after creating an order, run cleanup
      from apps.public.controller.cart_class import cleanupCarts
      cleanupCarts()
    return orders

  except models.Cart.DoesNotExist:
    return []

  except Exception as e:
    ExceptionHandler(e, "in order_class.getOrders")
    return []

def createFromCart(cart):
  from apps.communication.controller.email_class import Email
  from settings.people import Tom, Dan, Tifawt
  from apps.public.controller.cart_class import Cart

  orders = []

  try:
    cart = Cart(cart_id=cart.id)
    checkout_data = cart.getCheckoutData()

    for item in cart:
      if item.product.sold_at == None:
        orders.append(createFromCartItem(item, checkout_data))
        item.product.sold_at = timezone.now()
        item.product.save()
      else:
        email = Email(message="customer was just charged for a product someone else already bought")
        email.sendTo([Tom.email, Dan.email, Tifawt.email])

    if order_events.communicateOrdersCreated(orders):
      for order in orders:
        order.seller_notified_at = timezone.now()
        order.save()

  except Exception as e:
    ExceptionHandler(e, "in order_class.createFromCart")

  return orders

def createFromCartItem(item, checkout_data):
  order = models.Order(
    cart                = item.cart,
    products_charge     = item.product.price,
    anou_charge         = item.product.anou_fee,
    shipping_charge     = item.product.shipping_cost,
    total_charge        = item.product.intl_price,
    seller_paid_amount  = item.product.price + item.product.shipping_cost
  )
  order.save()
  order.products.add(item.product)
  return order

#class Order(object):
#  def __init__(self, order_id=None):
#    self.order = models.Order.objects.get(id=order_id)
#
#  def seller_confirmed(self):
#    if order_events.communicateOrderConfirmed(self.order):
#      self.order.is_seller_confirmed = True
#      self.order.save()
#    else:
#      raise Exception
#
#  def seller_shipped(self, tracking_number=None):
#    if order_events.communicateOrderShipped(self.order):
#      self.order.is_shipped = True
#      self.order.shipped_date = date.today()
#      if tracking_number:
#        self.order.tracking_number = tracking_number
#      self.order.save()
#    else:
#      raise Exception
#
#  def seller_paid(self):
#    if order_events.communicateOrderSellerPaid(self.order):
#      self.order.is_seller_paid = True
#      self.order.save()
#    else:
#      raise Exception
#
#  def customer_received(self):
#    self.order.is_received = True
#    self.order.received_date = date.today()
#    self.order.save()
#
#  def update(self):
#    pass
#
#  def refund(self):
#    pass
