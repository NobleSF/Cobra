# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='bcc_address',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='cc_address',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='email',
            name='from_address',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='email',
            name='to_address',
            field=models.EmailField(max_length=254),
        ),
    ]
