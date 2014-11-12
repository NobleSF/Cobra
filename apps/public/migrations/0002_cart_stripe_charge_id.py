# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='stripe_charge_id',
            field=models.CharField(max_length=35, null=True, blank=True),
            preserve_default=True,
        ),
    ]
