# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def copyColors(apps, schema_editor):
  Product = apps.get_model('seller', 'Product')
  OldColor = apps.get_model('admin', 'OldColor')
  NewColor = apps.get_model('common', 'NewColor')

  for oldcolor in OldColor.objects.all():
    newcolor, created = NewColor.objects.get_or_create(
                          name=oldcolor.name,
                          hex_value=oldcolor.hex_value
                        )

  for product in Product.objects.all():
    for oldcolor in product.oldcolors.all():
      newcolor, created = NewColor.objects.get_or_create(
                            name=oldcolor.name,
                            hex_value=oldcolor.hex_value
                          )
      product.newcolors.add(newcolor)

class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0009_product_newcolors'),
    ]

    operations = [
        migrations.RunPython(copyColors)
    ]
