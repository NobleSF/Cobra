# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0006_move_currency_model'),
        ('seller', '0005_auto_20150520_0803'),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=3)),
                ('exchange_rate_to_USD', models.FloatField(verbose_name=b'Exchange Rate')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        )
    ]

    operations = [
        migrations.SeparateDatabaseAndState(state_operations=state_operations)
    ]