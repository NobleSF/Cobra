# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0030_auto_20150526_0506'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='new_subject',
            field=models.SmallIntegerField(default=0, choices=[(1, b'photography'), (2, b'price'), (3, b'appeal')]),
            preserve_default=False,
        ),
    ]
