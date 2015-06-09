# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0009_auto_20150607_0813'),
        ('common', '0003_newcolor'),
        ('seller', '0008_rename_color_to_oldcolor'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='newcolors',
            field=models.ManyToManyField(related_name='products', to='common.NewColor'),
        ),
    ]
