def communicateOrdersCreated(orders):
  for order in orders:
    #send text to seller
    pass

  #send email to buyer
  return True

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

def test():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev@theanou.com'], fail_silently=False)
