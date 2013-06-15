from apps.public import models
from apps.communication.controller import events

class Order:
  def __init__(self, order_id):
    self.order = models.Order.objects.get(id=order_id)

  def createFromCart(self, cart):
    checkout_data = self.getCheckoutData(cart)

    orders = []
    for item in cart:
      orders.append(self.createFromCartItem(item, checkout_data))

    if events.communicateOrdersCreated(orders):
      for order in orders:
        order.is_seller_notified = True
        order.save()
    else:
      raise Exception

    return orders

  def createFromCartItem(self, item, checkout_data):
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

  def getCheckoutData(self, cart=None):
    from apps.wepay.api import WePay
    from settings.settings import WEPAY, PRODUCTION
    if not cart:
      cart = self.order.cart

    wepay = WePay(PRODUCTION, WEPAY['access_token'])
    wepay_response = wepay.call('/checkout', {
      'checkout_id': cart.wepay_checkout_id
    })

    #start with WePay data, then overwrite with our own.
    checkout_data = wepay_response

    #name and email
    if cart.name: checkout_data['name'] = cart.name
    else: checkout_data['name'] = wepay_response['payer_name']
    if cart.email: checkout_data['email'] = cart.email
    else: checkout_data['email'] = wepay_response['payer_email']

    #shipping address
    if cart.address1 and cart.city and cart.state and cart.postal_code:
      checkout_data['shipping_address']['address1']     = cart.address_1
      checkout_data['shipping_address']['address2']     = cart.address2
      checkout_data['shipping_address']['city']         = cart.city
      checkout_data['shipping_address']['state']        = cart.state
      checkout_data['shipping_address']['postal_code']  = cart.postal_code
      checkout_data['shipping_address']['country']      = cart.country
    elif wepay_response['shipping_address']['region'] or \
         wepay_response['shipping_address']['post_code']:
      # international address, all should match except region -> state, post_code -> postal_code
      checkout_data['shipping_address']['state'] = wepay_response['shipping_address']['region']
      checkout_data['shipping_address']['postal_code'] = wepay_response['shipping_address']['post_code']
    else:
      #US address, all should match up except zip -> postal_code
      checkout_data['shipping_address']['postal_code'] = wepay_response['shipping_address']['zip']

    return checkout_data

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
