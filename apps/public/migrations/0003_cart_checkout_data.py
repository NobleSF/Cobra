# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_cart_stripe_charge_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='checkout_data',
            field=jsonfield.fields.JSONField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
