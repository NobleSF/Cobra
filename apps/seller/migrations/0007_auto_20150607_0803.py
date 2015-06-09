# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0006_auto_20150607_0736'),
        ('common', '0002_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='country',
            field=models.ForeignKey(blank=True, to='common.Country', null=True),
        ),
        migrations.AlterField(
            model_name='shippingoption',
            name='country',
            field=models.ForeignKey(to='common.Country'),
        ),
    ]
