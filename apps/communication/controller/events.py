from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS

def communicateOrdersCreated(orders):
  try:
    for order in orders: #send SMS to seller for each order
      products_string = ""
      for product in order.products:
        products_string += str(product.id) + " "
      address_string = getCustomerAddressFromOrder(order, sms_format=True)
      msg = products_string + "\r\n" + address_string
      seller_phone = order.products.all()[0].seller.phone
      sendSMS(msg, seller_phone)

    #send email to buyer
    email = Email('order/created', orders)
    return email.sendTo(getCustomerEmailFromOrder(orders[0]))
    #returns True or exception string
  except Exception as e:
    return "error: " + str(e)

def updateOrder((product_id, action, data), gimme_reply_sms=False):
  #yes, it's gets a tuple and optional boolean
  if gimme_reply_sms:
    return "reply msg"
  else:
    return True

def communicateOrderConfirmed(order, gimme_reply_sms=False):
  try:
    sms_response_message = "Shukran"

    #send email to buyer
    email = Email('order/confirmed', order)
    email_success = email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_msg:
      return sms_response_message
    else:
      seller_phone = order.products.all()[0].seller.phone
      sms_success = sendSMS(sms_response_message, seller_phone)

      if (email_success == sms_success == True):
        return True
      else:
        return str(email_success) + str(sms_success)
        #each respectivly return True or exception str

  except Exception as e:
    return "error: " + str(e)

def communicateOrderShipped(order, reply_sms_sent=False):
  try:
    if not reply_sms_sent:
      msg = "Shukran"
      seller_phone = order.products.all()[0].seller.phone
      sendSMS(msg, seller_phone)

    #send email to buyer
    email = Email('order/shipped', order)
    return email.sendTo(getCustomerEmailFromOrder(order))
    #returns True or exception string
  except Exception as e:
    return "error: " + str(e)

def communicateOrderSellerPaid(order):
  try:
    if not reply_sms_sent:
      pass
      #sendSMS() to seller

  except Exception as e:
    return "error: " + str(e)

def communicateCustomerSubscribed(order):
  return True

#support functions
def getCustomerEmailFromOrder(order):
  if order.cart.name:
    return "%s <%s>" % (order.cart.name, order.cart.email)
  else:
    return order.cart.email

def getCustomerAddressFromOrder(order, sms_format=False):
  address  = str(order.cart.name)
  address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.address1)
  address += "\r\n" if sms_format else "<br>"

  if order.cart.address2:
    address += str(order.cart.address1)
    address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.city) + ","
  address += str(order.cart.state) + " "
  address += str(order.cart.postal_code)
  address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.country)
  return address

def test_email():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev+test@theanou.com'], fail_silently=False)
