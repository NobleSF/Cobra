# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations

def doStuff(apps, schema_editor):
  Order = apps.get_model("public", "Order")
  Checkout = apps.get_model("public", "Checkout")
  errors = []

  # order.products.first() -> order.product
  for order in Order.objects.all():
    try:
      order.product = order.products.first()
      order.save()
      order.products.clear()
    except Exception as e:
      errors.append("product for order %d: %s" % (order.id, str(e)))

  # checkout.cart.anou_checkout_id.startswith('MAN') -> checkout.is_manual_order = True
  for checkout in Checkout.objects.filter(cart__anou_checkout_id__isnull=False):
    if checkout.cart.anou_checkout_id.startswith('MAN'):
      try:
        checkout.payment_id = checkout.cart.anou_checkout_id
        checkout.is_manual_order = True
        checkout.save()
      except Exception as e:
        errors.append("manual order for checkout %d: %s" % (checkout.id, str(e)))
      try:
        checkout.total_paid = checkout.cart.summary()
        checkout.save()
      except Exception as e:
        errors.append("manual total_paid for checkout %d: %s" % (checkout.id, str(e)))

  # checkout.cart.checkout_data -> checkout.payment_data
  # checkout.cart.checkout_id -> checkout.payment_id
  for checkout in Checkout.objects.filter(cart__wepay_checkout_id__isnull=False):
    if checkout.cart.checkout_data:
      try:
        checkout.payment_data = checkout.cart.checkout_data
        checkout.payment_id = checkout.cart.wepay_checkout_id
        checkout.save()
      except Exception as e:
        errors.append("wepay checkout data for checkout %d: %s" % (checkout.id, str(e)))
      try:
        if checkout.payment_data.get('state') in ['captured', 'refunded']:
          checkout.total_paid = checkout.payment_data.get('amount')
          checkout.save()
      except Exception as e:
        errors.append("wepay total_paid for checkout %d: %s" % (checkout.id, str(e)))

  for checkout in Checkout.objects.filter(cart__stripe_charge_id__isnull=False):
    try:
      checkout.payment_data = checkout.cart.checkout_data
      checkout.payment_id = checkout.cart.stripe_charge_id
      checkout.save()
    except Exception as e:
      errors.append("stripe checkout data for checkout %d: %s" % (checkout.id, str(e)))
    try:
      checkout.total_paid = checkout.payment_data.get('amount')
      checkout.save()
    except Exception as e:
      errors.append("stripe payment amount for checkout %d: %s" % (checkout.id, str(e)))

  from apps.communication.controller.email_class import Email
  message = "<p>"
  for error in errors:
    message += str(error) + "<br>"
  message += "</p>"
  Email(message=message).sendTo(['dev@theanou.com'])

class Migration(migrations.Migration):

    dependencies = [
        ('public', '0014_auto_20141125_0231'),
    ]

    operations = [
      migrations.RunPython(doStuff),
    ]
