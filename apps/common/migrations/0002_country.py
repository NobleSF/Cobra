# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_import_currency_model'),
        ('seller', '0006_auto_20150607_0736'),
        ('admin', '0008_move_country_model'),

    ]

    state_operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('calling_code', models.IntegerField()),
                ('currency', models.ForeignKey(to='common.Currency')),
            ],
            options={
            },
            bases=(models.Model,),
        )
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]