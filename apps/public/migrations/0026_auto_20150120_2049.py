# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0025_commission_customer_confirmed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='estimated_artisan_price',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commission',
            name='price_adjustment',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commission',
            name='estimated_display_price',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='commission',
            name='estimated_weight',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
