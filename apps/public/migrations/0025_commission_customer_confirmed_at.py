# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0024_auto_20141230_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='customer_confirmed_at',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
