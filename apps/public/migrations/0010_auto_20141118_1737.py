from __future__ import unicode_literals
from django.db import models, migrations

def createCheckoutForEachPaidCart(apps, schema_editor):
  #clean up checked out carts without orders
  Cart = apps.get_model("public", "Cart")
  for cart in Cart.objects.filter(checked_out=True):
    if len(cart.orders.all()) < 1:
      cart.delete()
    if not getCheckoutId(cart):
      cart.delete()

  Checkout = apps.get_model("public", "Checkout")
  for cart in Cart.objects.filter(checked_out=True):
    #create a checkout for each cart that has been checked out (paid)
    if getCheckoutId(cart):
      checkout = Checkout(cart=cart)
      checkout.checkout_id    = getCheckoutId(cart)
      checkout.checkout_data  = cart.checkout_data
      checkout.receipt        = cart.receipt
      checkout.notes          = cart.notes
      checkout.save()
      #save cart's orders to the new checkout for that cart
      #the cart column on the order will be deleted soon
      for order in cart.orders.all():
        order.checkout_id = checkout.id
        order.save()

      if cart.stripe_charge_id and checkout.checkout_data:
        #save Stripe checkout_data into checkout model values
        checkout.total_charge     = float(checkout.checkout_data.get('amount'))/100
        checkout.total_discount   = 0
        checkout.total_paid       = float(checkout.checkout_data.get('amount'))/100 if checkout.checkout_data.get('captured') else 0
        if checkout.checkout_data.get('refunded'):
          try:
            refund_amounts = [refund['amount'] for refund in checkout.checkout_data['refund']['data']]
            checkout.total_refunded = sum(refund_amounts) / 100
          except: pass
        checkout.currency = "USD"
        checkout.save()

      elif cart.wepay_checkout_id and checkout.checkout_data:
        #save WePay checkout_data into checkout model values
        checkout.total_charge     = checkout.checkout_data.get('amount')
        checkout.total_discount   = 0
        checkout.total_paid       = checkout.checkout_data.get('amount') if checkout.checkout_data.get('state') in ['captured', 'refunded'] else 0
        checkout.total_refunded   = checkout.checkout_data.get('amount_refunded')
        checkout.save()

def getCheckoutId(cart):
  if cart.wepay_checkout_id:
    return cart.wepay_checkout_id
  elif cart.anou_checkout_id:
    return cart.anou_checkout_id
  elif cart.stripe_charge_id:
    return cart.stripe_charge_id[3:]
  else:
    return False

class Migration(migrations.Migration):
  dependencies = [
    ('public', '0009_auto_20141118_1735'),
  ]
  operations = [
    migrations.RunPython(createCheckoutForEachPaidCart),
  ]