# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0006_order_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='currency_string',
            field=models.CharField(default=b'USD', max_length=3),
            preserve_default=True,
        ),
    ]
