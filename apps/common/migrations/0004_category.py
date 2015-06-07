# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_newcolor'),
        ('seller', '0014_auto_20150607_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plural_name', models.CharField(max_length=50)),
                ('keywords', models.CharField(max_length=50, null=True, blank=True)),
                ('parent_category', models.IntegerField(null=True)),
                ('ordering_name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['ordering_name'],
            },
        ),
    ]
