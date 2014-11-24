# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0011_auto_20141118_2236'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='is_manual_order',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='cart',
            field=models.ForeignKey(related_name='items', to='public.Cart'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.ForeignKey(related_name='items_in_carts', to='seller.Product'),
            preserve_default=True,
        ),
    ]
