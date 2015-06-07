# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0010_copy_color_relationships'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='oldcolors',
        ),
    ]
