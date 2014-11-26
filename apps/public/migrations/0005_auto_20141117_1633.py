from __future__ import unicode_literals
from django.db import models, migrations


def saveFirstOfProductsAsProduct(apps, schema_editor):
  # We can't import the Person model directly as it may be a newer
  # version than this migration expects. We use the historical version.
  Order = apps.get_model("public", "Order")
  for order in Order.objects.all():
    try:
      if len(order.products.all()):
        order.product = order.products.all()[0]
        order.save()
    except: pass

class Migration(migrations.Migration):
  dependencies = [
    ('public', '0004_auto_20141117_1633'),
  ]

  operations = [
    migrations.RunPython(saveFirstOfProductsAsProduct),
  ]
