# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_auto_20150520_0803'),
        ('common', '0001_import_currency_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='country',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shippingoption',
            name='country',
            field=models.IntegerField(),
        ),
    ]
