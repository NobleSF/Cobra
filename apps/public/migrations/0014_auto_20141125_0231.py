# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0013_auto_20141124_1622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AlterField(
            model_name='order',
            name='checkout',
            field=models.ForeignKey(related_name='orders', default=1, to='public.Checkout'),
            preserve_default=False,
        ),
    ]
