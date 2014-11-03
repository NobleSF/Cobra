# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_address', models.EmailField(max_length=75)),
                ('to_address', models.EmailField(max_length=75)),
                ('cc_address', models.EmailField(max_length=75, null=True, blank=True)),
                ('bcc_address', models.EmailField(max_length=75, null=True, blank=True)),
                ('subject', models.CharField(max_length=200)),
                ('html_body', models.TextField(null=True, blank=True)),
                ('text_body', models.TextField(null=True, blank=True)),
                ('attachment', models.URLField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, to='public.Order', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_number', models.CharField(max_length=15)),
                ('to_number', models.CharField(max_length=15)),
                ('message', models.CharField(max_length=160)),
                ('auto_reply', models.CharField(max_length=160, null=True, blank=True)),
                ('telerivet_id', models.CharField(max_length=34)),
                ('status', models.CharField(max_length=15, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(blank=True, to='public.Order', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
