from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS, sendSMSForOrder
from settings.settings import DEBUG
from apps.communication.models import SMS

def communicateOrdersCreated(orders):
  try:
    for order in orders: #send SMS to seller for each order
      products_string = ""
      for product in order.products.all():
        products_string += "%d  " % product.id

        #message each artisan that their product has sold and for how much
        artisan_msg = "%d \r\n %d Dh" % (product.id, product.price)
        for artisan in product.assets.filter(ilk='artisan'):
          pass
          #artisan assets need phone numbers
          #sendSMS(artisan_msg, artisan.phone)

      #message the seller with the address
      address_string = getCustomerAddressFromOrder(order, sms_format=True)
      seller_msg = products_string + "\r\n" + address_string
      seller_phone = order.products.all()[0].seller.phone
      sms = sendSMSForOrder(seller_msg, seller_phone, order)
      if not isinstance(sms, SMS):
        error_message = sms #received in place of SMS object
        #todo: email tom here

      #notify Brahim
      try:
        email = Email('order/created_copy_director', order)
        email.sendTo("brahim@theanou.com")
      except: pass
        #todo: emial tom about this problem

    #send email to buyer
    email = Email('order/created', orders)
    return email.sendTo(getCustomerEmailFromOrder(orders[0]))
    #returns True or exception string
  except Exception as e:
    return "error: " + str(e)

def updateOrder((product_id, data), gimme_reply_sms=False):
  #gets a tuple (of id and data dict) and optional boolean
  from datetime import datetime
  from apps.public.models import Order
  from apps.seller.models import Product

  #if product_id: #we should always have a product id
  try:
    product = Product.objects.get(id=product_id)
    order = product.order_set.all()[0]

    if data.get('remove'): #the product should be removed
      if product.order_set.all():
        if order.is_seller_confirmed:
          reply = 'xata'
        else:
          reply = 'shukran'
          #todo: email dan or tom, or text brahim
          #cancel order and tell customer

      else:
        product.deactive_at = datetime.now()
        product.save()
        reply = 'shukran'

    else: #update the order of that product_id
      reply = str(product_id) + " "

      if data.get('tracking_number'): #if they provide a tracking number
        #the order is both confirmed and shipped
        if not order.is_seller_confirmed: order.seller_confirmed_at = datetime.now()
        order.shipped_at = datetime.now()
        order.tracking_number = data.get('tracking_number')
        order.save()
        reply += communicateOrderShipped(order, gimme_reply_sms)

      elif order.is_seller_confirmed and not order.is_shipped: #if order already confirmed
        #confirm it is shipped
        order.shipped_at = datetime.now()
        order.save()
        reply += communicateOrderShipped(order, gimme_reply_sms)

      elif not order.is_seller_confirmed: #if the order is not yet confirmed
        #confirm the order
        order.seller_confirmed_at = datetime.now()
        order.save()
        reply += communicateOrderConfirmed(order, gimme_reply_sms)

      else: #if everything is already done
        if DEBUG: reply = '(safi) redundant confirmation'
        else: reply += "safi"

  except Proudct.DoesNotExist:
    if DEBUG: reply = '(xata) This product does not exist.'
    else: reply = 'xata'

  except Exception as e:
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
    email_success = email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms and (email_success == True):
      return sms_reply
    elif gimme_reply_sms:
      #error message in email_success string
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sms = sendSMS(sms_reply, seller_phone)

      if (email_success == True) and isinstance(sms, SMS) :
        return True
      else:
        return str(email_success) + str(sms)
        #each respectivly return True or exception str

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
    email_success = email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms and (email_success == True):
      return sms_reply
    elif gimme_reply_sms:
      #error message in email_success string
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sms = sendSMS(sms_reply, seller_phone)

      if (email_success == True) and isinstance(sms, SMS):
        return True
      else:
        return str(email_success) + str(sms)
        #each respectivly return True or exception str

  except Exception as e:
    if DEBUG: return '(xata) ' + str(e)
    else:
      return 'xata'
      #todo: send error data to dev

def communicateOrderSellerPaid(order):
  try:
    pass
    #sendSMS() to seller

  except Exception as e:
    return "error: " + str(e)

#support functions

def getCustomerEmailFromOrder(order):
  if order.cart.name:
    return "%s <%s>" % (order.cart.name, order.cart.email)
  else:
    return order.cart.email

def getCustomerAddressFromOrder(order, sms_format=False):
  address  = "\r\n" if sms_format else ""
  address += str(order.cart.name)
  address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.address1)
  address += "\r\n" if sms_format else "<br>"

  if order.cart.address2:
    address += str(order.cart.address1)
    address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.city) + ", "
  address += str(order.cart.state) + " "
  address += str(order.cart.postal_code)
  address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.country)
  return address
