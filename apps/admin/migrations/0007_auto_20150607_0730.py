# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_move_currency_model'),
        ('common', '0001_import_currency_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='currency',
            field=models.ForeignKey(to='common.Currency'),
        ),
    ]
