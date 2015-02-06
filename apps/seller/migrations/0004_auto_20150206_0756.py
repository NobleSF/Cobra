# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_auto_20150106_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='rank',
            field=models.SmallIntegerField(null=True),
            preserve_default=True,
        ),
    ]
