# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0004_auto_20150522_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='currency',
            field=models.IntegerField(),
        ),
    ]
