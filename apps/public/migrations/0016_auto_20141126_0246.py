# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def doStuff(apps, schema_editor):
  Order = apps.get_model("public", "Order")
  Checkout = apps.get_model("public", "Checkout")

  for o in Order.objects.all():
    try:
      o.public_id = "R%d" % o.pk
      o.save()
    except: pass

  for c in Checkout.objects.all():
    try:
      c.public_id = "T%d" % c.pk
      c.save()
    except: pass

class Migration(migrations.Migration):

  dependencies = [
    ('public', '0015_auto_20141126_0041'),
  ]

  operations = [
    migrations.RunPython(doStuff),
  ]
