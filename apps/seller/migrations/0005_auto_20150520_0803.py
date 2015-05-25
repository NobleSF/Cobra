# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0004_auto_20150206_0756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='categories',
            field=models.ManyToManyField(to='admin.Category'),
        ),
    ]
