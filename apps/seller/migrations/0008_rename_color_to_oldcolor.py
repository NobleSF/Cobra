# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0007_auto_20150607_0803'),
        ('admin', '0009_auto_20150607_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='colors',
            new_name='oldcolors',
        ),
    ]
