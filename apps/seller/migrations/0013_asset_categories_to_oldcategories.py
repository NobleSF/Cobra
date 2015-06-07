# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0012_product_oldcolors_to_colors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='categories',
            new_name='oldcategories',
        ),
    ]
