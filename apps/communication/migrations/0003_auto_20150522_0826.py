# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0002_auto_20150520_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='bcc_address',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='email',
            name='cc_address',
            field=models.EmailField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='email',
            name='from_address',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='email',
            name='to_address',
            field=models.EmailField(max_length=75),
            preserve_default=True,
        ),
    ]
