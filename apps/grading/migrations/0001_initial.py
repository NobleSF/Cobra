# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_auto_20150520_0803'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('initial_points', models.BigIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('voided_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.SmallIntegerField(unique=True, choices=[(0, b'product-add'), (1, b'product-edit'), (3, b'sms-order'), (4, b'sms-shipping'), (5, b'rating-photography'), (6, b'rating-appeal'), (7, b'rating-appeal')])),
                ('max_points', models.BigIntegerField()),
                ('has_spread', models.BooleanField(default=False)),
                ('min_points', models.BigIntegerField(null=True, blank=True)),
                ('count_limit', models.SmallIntegerField(default=0)),
                ('is_penalty', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='action_type',
            field=models.ForeignKey(to='grading.ActionType'),
        ),
        migrations.AddField(
            model_name='action',
            name='seller',
            field=models.ForeignKey(related_name='actions', to='seller.Seller'),
        ),
    ]
