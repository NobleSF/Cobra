from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS

def communicateOrdersCreated(orders):
  try:
    for order in orders:
      #sendSMS() to seller
      pass

    #send email to buyer
    email = Email('order/created', orders)
    return email.sendTo(getCustomerEmailFromOrder(orders[0]))
  except Exception as e:
    return str(e)

def communicateOrderConfirmed(order):
  #send reply text to seller
  #send email to buyer
  return True

def communicateOrderShipped(order):
  #send reply text to seller
  #send email to buyer
  return True

def communicateOrderSellerPaid(order):
  #send text to seller
  return True

def getCustomerEmailFromOrder(order):
  if order.cart.name:
    return "%s <%s>" % (order.cart.name, order.cart.email)
  else:
    return order.cart.email

def test():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev+test@theanou.com'], fail_silently=False)
