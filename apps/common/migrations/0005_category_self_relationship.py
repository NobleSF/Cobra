# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_category'),
        ('seller', '0015_asset_newcategories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(related_name='sub_categories', blank=True, to='common.Category', null=True),
        ),
    ]
