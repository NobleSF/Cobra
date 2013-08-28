from apps.public import models
from apps.communication.controller import order_events
from datetime import datetime

def getOrders(checkout_id):
  try:
    cart = models.Cart.objects.get(wepay_checkout_id = checkout_id)
  except:
    cart = models.Cart.objects.get(anou_checkout_id = checkout_id)

  orders = cart.order_set.all()
  if not orders:
    orders = createFromCart(cart)
    #after creating an order, run cleanup
    from apps.public.controller.cart_class import cleanupCarts
    cleanupCarts()
  return orders

def createFromCart(cart):
  from apps.public.controller.cart_class import Cart
  cart = Cart(cart_id=cart.id)
  checkout_data = cart.getCheckoutData()

  orders = []
  for item in cart: #or for item in cart.cart.item_set.all()
    if item.product.sold_at == None:
      orders.append(createFromCartItem(item, checkout_data))
      item.product.sold_at = datetime.now()
      item.product.save()
    else:
      #we have a problem, the customer was just charged for a product someone else already bought
      #todo: to notify someone about this item.product
      pass

  if order_events.communicateOrdersCreated(orders) == True:
    for order in orders:
      order.seller_notified_at = datetime.now()
      order.save()
  else:
    pass
    #todo: email Tom the error response

  return orders

def createFromCartItem(item, checkout_data):
  order = models.Order(
    cart                = item.cart,
    products_charge     = item.product.price,
    anou_charge         = item.product.anou_fee,
    shipping_charge     = item.product.shipping_cost,
    total_charge        = item.product.local_price,
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
#    from datetime import date
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
#    from datetime import date
#    self.order.is_received = True
#    self.order.received_date = date.today()
#    self.order.save()
#
#  def update(self):
#    pass
#
#  def refund(self):
#    pass
