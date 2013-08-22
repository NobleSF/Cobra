from apps.communication.controller.email_class import Email
from apps.communication.controller.sms import sendSMS
from settings.settings import DEBUG
from settings import people

def createdSeller(product):
 pass

def activatedProduct(product):
  email = Email('product/activated', product)
  email.sendTo(people.Dan.email)

#translation event functions
