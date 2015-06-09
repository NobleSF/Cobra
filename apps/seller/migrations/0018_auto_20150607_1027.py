# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0017_remove_asset_oldcategories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='newcategories',
            new_name='categories',
        ),
    ]
