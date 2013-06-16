from apps.public import models
from apps.communication.controller import events

def getOrders(wepay_checkout_id):
  cart = models.Cart.objects.get(wepay_checkout_id = wepay_checkout_id)
  orders = cart.order_set.all()
  if not orders:
    orders = createFromCart(cart)
  return orders

def createFromCart(cart):
  from apps.public.controller.cart_class import Cart
  cart = Cart(cart_id=cart.id)
  checkout_data = cart.getCheckoutData()

  orders = []
  for item in cart: #or for item in cart.cart.item_set.all()
    orders.append(createFromCartItem(item, checkout_data))

  if events.communicateOrdersCreated(orders):
    for order in orders:
      order.is_seller_notified = True
      order.save()
  else:
    raise Exception

  return orders

def createFromCartItem(item, checkout_data):
  order = models.Order(
    cart            = item.cart,
    products_charge = item.product.price,
    anou_charge     = item.product.anou_fee(),
    shipping_charge = item.product.shipping_cost(),
    total_charge    = item.product.local_price()
  )
  order.save()
  order.products.add(item.product)
  return order

class Order:
  def __init__(self, order_id=None):
    self.order = models.Order.objects.get(id=order_id)

  def seller_confirmed(self):
    if events.communicateOrderConfirmed(self.order):
      self.order.is_seller_confirmed = True
      self.order.save()
    else:
      raise Exception

  def seller_shipped(self, tracking_number=None):
    from datetime import date
    if events.communicateOrderShipped(self.order):
      self.order.is_shipped = True
      self.order.shipped_date = date.today()
      if tracking_number:
        self.order.tracking_number = tracking_number
      self.order.save()
    else:
      raise Exception

  def seller_paid(self):
    if events.communicateOrderSellerPaid(self.order):
      self.order.is_seller_paid = True
      self.order.save()
    else:
      raise Exception

  def customer_received(self):
    from datetime import date
    self.order.is_received = True
    self.order.received_date = date.today()
    self.order.save()

  def update(self):
    pass

  def refund(self):
    pass
