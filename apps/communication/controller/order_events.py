from apps.admin.utils.exception_handling import ExceptionHandler
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
          ExceptionHandler(e, "in order_events.communicateOrdersCreated-A")

      #message the seller with the address
      address_string = order.cart.shipping_address.replace('\n','\n\r')
      seller_msg = products_string + "\r\n" + address_string
      seller_phone = order.seller.phone
      sendSMSForOrder(seller_msg, seller_phone, order)

      #notify the team
      try:
        order.seller_msg = seller_msg.replace('\n', '<br>')
        emails = [people.Dan.email, people.Brahim.email,
                  people.Rabha.email, people.Kenza.email, people.Mustapha.email]
        for address in emails:
          Email('order/created_copy_director', order).sendTo(address)

      except Exception as e:
        ExceptionHandler(e, "in order_events.communicateOrdersCreated-B")

    #send email to buyer
    email = Email('order/created', orders)
    email.assignToOrder(orders[0])
    email.sendTo(orders[0].cart.email_with_name)
    return True
  except Exception as e:
    ExceptionHandler(e, "in order_events.communicateOrdersCreated-C")
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
  from apps.seller.models.product import Product

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
    email.sendTo(order.cart.email_with_name)

    if gimme_reply_sms:
      return sms_reply

    else:
      seller_phone = order.seller.phone
      sendSMSForOrder(sms_reply, seller_phone, order)

  except Exception as e:
    if DEBUG: return '(xata) ' + str(e)
    else:
      return 'xata'
      ExceptionHandler(e, "in order_events.communicateOrderConfimed")

def communicateOrderShipped(order, gimme_reply_sms=False):
  try:
    if DEBUG: sms_reply = '(shukran) order confirmed shipped'
    else: sms_reply = 'shukran'

    #send email to buyer
    email = Email('order/shipped', order)
    email.assignToOrder(order)
    email.sendTo(order.cart.email_with_name)

    if gimme_reply_sms:
      return sms_reply

    else:
      seller_phone = order.seller.phone
      sendSMSForOrder(sms_reply, seller_phone, order)

  except Exception as e:
    if DEBUG: return '(xata) ' + str(e)
    else:
      return 'xata'
      ExceptionHandler(e, "in order_events.communicateOrderShipped")

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
