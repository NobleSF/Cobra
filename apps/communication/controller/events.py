def communicateOrderCreated(order):
  #send text to seller
  #send email to buyer
  pass

def communicateOrderConfirmed(order):
  #send reply text to seller
  #send email to buyer
  pass

def communicateOrderShipped(order):
  #send reply text to seller
  #send email to buyer
  pass

def communicateOrderArtisansPaid(order):
  #send text to seller
  pass

def test():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev@theanou.com'], fail_silently=False)
