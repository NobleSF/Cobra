# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0022_commission_requirement_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='commission',
            name='progression',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
