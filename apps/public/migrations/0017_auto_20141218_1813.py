# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20141218_1813'),
        ('public', '0016_auto_20141126_0246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('quantity', models.SmallIntegerField(default=1)),
                ('length', models.IntegerField(null=True, blank=True)),
                ('width', models.IntegerField(null=True, blank=True)),
                ('estimated_price', models.SmallIntegerField(null=True, blank=True)),
                ('estimated_weight', models.SmallIntegerField(null=True, blank=True)),
                ('estimated_completion_date', models.DateTimeField(null=True, blank=True)),
                ('artisan_confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('invoice_sent_at', models.DateTimeField(null=True, blank=True)),
                ('invoice_paid_at', models.DateTimeField(null=True, blank=True)),
                ('artisan_notified_at', models.DateTimeField(null=True, blank=True)),
                ('in_progress_at', models.DateTimeField(null=True, blank=True)),
                ('complete_at', models.DateTimeField(null=True, blank=True)),
                ('shipped_at', models.DateTimeField(null=True, blank=True)),
                ('canceled_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_product', models.ForeignKey(related_name='commissions', to='seller.Product', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('address_name', models.CharField(max_length=100, null=True, blank=True)),
                ('address1', models.CharField(max_length=100, null=True, blank=True)),
                ('address2', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('state', models.CharField(max_length=50, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=15, null=True, blank=True)),
                ('country', models.CharField(max_length=50, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='commission',
            name='customer',
            field=models.ForeignKey(related_name='commission', to='public.Customer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commission',
            name='product',
            field=models.OneToOneField(related_name='commission', to='seller.Product'),
            preserve_default=True,
        ),
    ]
