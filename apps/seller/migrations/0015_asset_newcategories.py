# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_category'),
        ('seller', '0014_auto_20150607_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='newcategories',
            field=models.ManyToManyField(to='common.Category'),
        ),
    ]
