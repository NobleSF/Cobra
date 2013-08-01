from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS

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
      success = sendSMS(seller_msg, seller_phone)
      if success is not True:
        error_message = success #got stored in place of True
        #todo: email tom here

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

    if data.get('remove'): #the product should be removed
      if product.order_set.all():
        order = product.order_set.all()[0]
        if not order.is_seller_confirmed:
          pass #cancel order and tell customer
        reply = 'xata'

      else:
        product.is_active = False
        product.save()
        reply = 'shukran'

    else: #update the order of that product_id
      order = Order.objects.filter(product=product)
      tracking_number = data.get('tracking_number')
      reply = str(product_id) + " "

      if tracking_number: #if they provide a tracking number
        #the order is both confirmed and shipped
        order.is_seller_confirmed = order.is_shipped = True
        order.shipped_date = datetime.today()
        order.tracking_number = tracking_number
        order.save()
        reply += communicateOrderShipped(order, gimme_reply_sms)

      elif order.is_seller_confirmed: #if they have already confirmed the order
        #confirm it is shipped
        order.is_shipped = True
        order.shipped_date = datetime.today()
        order.save()
        reply += communicateOrderShipped(order, gimme_reply_sms)

      elif not order.is_seller_confirmed: #if the order is not yet confirmed
        #confirm the order
        order.is_seller_confirmed = True
        order.save()
        reply += communicateOrderConfirmed(order, gimme_reply_sms)

      else: #if everything is already done
        #their message was redundant
        reply += "safi"

      #order.save()

  except:
    pass

  if gimme_reply_sms:
    return reply
  else:
    #send the reply message to the seller
    return True

def communicateOrderConfirmed(order, gimme_reply_sms=False):
  try:
    sms_reply = "shukran"

    #send email to buyer
    email = Email('order/confirmed', order)
    email_success = email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms and (email_success == True):
      return sms_reply
    elif gimmer_reply_sms:
      #error message in email_success string
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sms_success = sendSMS(sms_reply, seller_phone)

      if (email_success == sms_success == True):
        return True
      else:
        return str(email_success) + str(sms_success)
        #each respectivly return True or exception str

  except Exception as e:
    return "error: " + str(e)

def communicateOrderShipped(order, gimme_reply_sms=False):
  try:
    sms_reply = "shukran"

    #send email to buyer
    email = Email('order/shipped', order)
    email_success = email.sendTo(getCustomerEmailFromOrder(order))

    if gimme_reply_sms and (email_success == True):
      return sms_reply
    elif gimmer_reply_sms:
      #error message in email_success string
      return sms_reply

    else:
      seller_phone = order.products.all()[0].seller.phone
      sms_success = sendSMS(msg, seller_phone)

      if (email_success == sms_success == True):
        return True
      else:
        return str(email_success) + str(sms_success)
        #each respectivly return True or exception str

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

  address += str(order.cart.city) + ", "
  address += str(order.cart.state) + " "
  address += str(order.cart.postal_code)
  address += "\r\n" if sms_format else "<br>"

  address += str(order.cart.country)
  return address

def test_email():
  from django.core.mail import send_mail
  send_mail('Subject here', 'Here is the message.', 'hello@theanou.com', ['dev+test@theanou.com'], fail_silently=False)
