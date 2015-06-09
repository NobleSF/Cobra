# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0013_asset_categories_to_oldcategories'),
        ('admin', '0012_rename_category_to_oldcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='oldcategories',
            field=models.ManyToManyField(to='admin.OldCategory'),
        ),
    ]
