# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0011_remove_product_oldcolors'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='newcolors',
            new_name='colors',
        ),
    ]
