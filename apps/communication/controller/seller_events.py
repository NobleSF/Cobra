from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS
from apps.communication.controller import order_events
from settings.settings import DEBUG
from settings import people

def createdSeller(account):
 pass

def activatedProduct(product):
  Email('product/activated', product).sendTo(people.Dan.email)

def deactivateProduct(product):
  from apps.seller.controller.product_class import Product

  if product.order_set.all():
    order_events.cancelOrder(product.order_set.all()[0])

  product = Product(product=product)#use Product class, not model object
  product.deactivate()

  message = "product %d has been removed by seller" % product.product.id
  Email(message=message).sendTo(people.Dan.email)

#translation event functions
