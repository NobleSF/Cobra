# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0011_category_self_relation_to_int'),
        ('seller', '0013_asset_categories_to_oldcategories'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='OldCategory',
        ),
    ]
