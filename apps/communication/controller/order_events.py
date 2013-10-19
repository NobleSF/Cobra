from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS, sendSMSForOrder
from apps.communication.models import SMS
from settings.settings import DEBUG
from settings import people
from django.utils import timezone

def communicateOrdersCreated(orders):
  try:
    for order in orders: #send SMS to seller for each order
      products_string = ""
      for product in order.products.all():
        products_string += "%d  " % product.id

        try: #message each artisan that their product has sold and for how much
          artisan_msg = "%d \r\n %d Dh" % (product.id, product.price)
          for artisan in product.assets.filter(ilk='artisan'):
            sendSMSForOrder(artisan_msg, artisan.phone, order)
        except Exception as e:
          Email(message="error sending SMS to artisans: "+str(e)).sendTo(people.Tom.email)

      #message the seller with the address
      address_string = getCustomerAddressFromOrder(order, sms_format=True)
      seller_msg = products_string + "\r\n" + address_string
      seller_phone = order.products.all()[0].seller.phone
      sendSMSForOrder(seller_msg, seller_phone, order)

      #notify Brahim
      try:
        order.seller_msg = seller_msg.replace('\r\n', '<br>')
        Email('order/created_copy_director', order).sendTo(people.Brahim.email)
      except Exception as e:
        Email(message="error sending copy to Brahim: "+str(e)).sendTo(people.Tom.email)

    #send email to buyer
    email = Email('order/created', orders)
    email.assignToOrder(orders[0])
    email.sendTo(getCustomerEmailFromOrder(orders[0]))
    return True
  except Exception as e:
    try:
      Email(message="error in communicateOrdersCreated: "+str(e)).sendTo(people.Tom.email)
    except: pass
    return False

def updateOrder((product_id, data), gimme_reply_sms=False):
  """
      gets a tuple of (id, data-dict) plus optional boolean
      product_id should have already been validated
      Step 1. If there is a tracking number, add it and promote the order to shipped
      Step 2. Else if already confirmed and not shipped, promote to shipped
      Step 3. Else if not confirmed, promote to confirmed
      Step 4. Else we can't go any further

  """
  from apps.public.models import Order
  from apps.seller.models import Product

  try:
    product = Product.objects.get(id=product_id)
    order = product.order_set.all()[0]

    reply = str(product_id) + " "

    if data.get('tracking_number'): #if tracking number provided
      #the order is both confirmed and shipped
      if not order.is_seller_confirmed: order.seller_confirmed_at = timezone.now()
      order.shipped_at = timezone.now()
      order.tracking_number = data.get('tracking_number')
      order.save()
      reply += communicateOrderShipped(order, gimme_reply_sms)

    elif order.is_seller_confirmed and not order.is_shipped: #if order already confirmed
      #confirm it is shipped
      order.shipped_at = timezone.now()
      order.save()
      reply += communicateOrderShipped(order, gimme_reply_sms)

    elif not order.is_seller_confirmed: #if the order is not yet confirmed
      #confirm the order
      order.seller_confirmed_at = timezone.now()
      order.save()
      reply += communicateOrderConfirmed(order, gimme_reply_sms)

    else: #if everything is already done
      if DEBUG: reply = '(safi) redundant confirmation'
      else: reply += "safi"

  except Exception as e:
    #primary scenario is product does not belong to any orders
    if DEBUG: reply = "(xata) " + str(e)
    else: reply = 'xata'

  if gimme_reply_sms:
    return (reply[:158] + '..') if len(reply)>160 else reply
  else:
    #send the reply message to the seller
    return True

def communicateOrderConfirmed(order, gimme_reply_sms=False):
  try:
    if DEBUG: sms_reply = '(shukran) order confirmed'
    else: sms_reply = 'shukran'

    #send email to buyer
    email = Email('order/confirmed', order)
    email.assignToOrder(order)
    email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms:
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sendSMSForOrder(sms_reply, seller_phone, order)

  except Exception as e:
    if DEBUG: return '(xata) ' + str(e)
    else:
      return 'xata'
      #todo: send error data to dev

def communicateOrderShipped(order, gimme_reply_sms=False):
  try:
    if DEBUG: sms_reply = '(shukran) order confirmed shipped'
    else: sms_reply = 'shukran'

    #send email to buyer
    email = Email('order/shipped', order)
    email.assignToOrder(order)
    email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms:
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sendSMSForOrder(sms_reply, seller_phone, order)

  except Exception as e:
    if DEBUG: return '(xata) ' + str(e)
    else:
      return 'xata'
      #todo: send error data to dev

def communicateOrderSellerPaid(order):
  try:
    pass
    #sendSMSForOrder() to seller

  except Exception as e:
    return "error: " + str(e)

def cancelOrder(order):
  message = 'Cancel order %d, Confirmation# %d' % (order.id, order.cart.checkout_id)
  email = Email(message=message)
  email.assignToOrder(order)
  email.sendTo((people.Dan.email,people.Tom.email))
  #todo: email customer

#support functions

def getCustomerEmailFromOrder(order):
  if order.cart.name:
    return "%s <%s>" % (order.cart.name, order.cart.email)
  else:
    return order.cart.email

def getCustomerAddressFromOrder(order, sms_format=False):
  address  = "\r\n" if sms_format else ""

  if order.cart.address_name:
    address += str(order.cart.address_name)
    address += "\r\n" if sms_format else "<br>"
  elif order.cart.name:
    address += str(order.cart.name)
    address += "\r\n" if sms_format else "<br>"

  if order.cart.address1:
    address += str(order.cart.address1)
    address += "\r\n" if sms_format else "<br>"

  if order.cart.address2:
    address += str(order.cart.address2)
    address += "\r\n" if sms_format else "<br>"

  if order.cart.city:
    address += str(order.cart.city) + ", "

  if order.cart.state:
    address += str(order.cart.state) + " "

  if order.cart.postal_code:
    address += str(order.cart.postal_code)

  if order.cart.country:
    address += "\r\n" if sms_format else "<br>"
    address += str(order.cart.country)

  return address
