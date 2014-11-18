from __future__ import unicode_literals

from django.db import models, migrations

def createPublicIds(apps, schema_editor):

  Order = apps.get_model("public", "Order")
  for order in Order.objects.all():
    order.save()#runs post_save signal

  Checkout = apps.get_model("public", "Checkout")
  for checkout in Checkout.objects.all():
    checkout.save()#runs post_save signal


class Migration(migrations.Migration):
  dependencies = [
    ('public', '0010_auto_20141118_1737'),
  ]

  operations = [
    migrations.AddField(
        model_name='order',
        name='public_id',
        field=models.CharField(max_length=8, null=True, blank=True),
        preserve_default=True,
    ),
    migrations.AlterField(
        model_name='checkout',
        name='public_id',
        field=models.CharField(max_length=8, null=True, blank=True),
        preserve_default=True,
    ),
    migrations.RunPython(createPublicIds),
  ]
