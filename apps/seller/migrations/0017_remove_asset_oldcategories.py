# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0016_copy_asset_category_relationships'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='oldcategories',
        ),
    ]
