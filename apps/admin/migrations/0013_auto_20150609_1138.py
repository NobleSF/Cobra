# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0012_rename_category_to_oldcategory'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='OldAccount',
        ),
    ]
