# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, unique=True, null=True, blank=True)),
                ('password', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, unique=True, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, unique=True, null=True, blank=True)),
                ('bank_name', models.CharField(max_length=50, null=True, blank=True)),
                ('bank_account', models.CharField(max_length=100, null=True, blank=True)),
                ('admin_type', models.CharField(max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('plural_name', models.CharField(max_length=50)),
                ('keywords', models.CharField(max_length=50, null=True, blank=True)),
                ('ordering_name', models.CharField(max_length=100)),
                ('parent_category', models.ForeignKey(related_name='sub_categories', blank=True, to='admin.Category', null=True)),
            ],
            options={
                'ordering': ['ordering_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=15)),
                ('hex_value', models.CharField(max_length=6)),
            ],
            options={
                'ordering': ['id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3)),
                ('calling_code', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        ),
        migrations.CreateModel(
            name='RatingSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='country',
            name='currency',
            field=models.ForeignKey(to='admin.Currency'),
            preserve_default=True,
        ),
    ]
