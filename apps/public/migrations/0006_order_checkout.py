# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0005_auto_20141117_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkout',
            field=models.ForeignKey(related_name='orders', blank=True, to='public.Checkout', null=True),
            preserve_default=True,
        ),
    ]
