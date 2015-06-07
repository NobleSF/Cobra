# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('hex_value', models.CharField(max_length=6)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
