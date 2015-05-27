# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0005_auto_20150520_0803'),
        ('public', '0030_auto_20150526_0506'),
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
                ('estimated_artisan_price', models.IntegerField(null=True, blank=True)),
                ('estimated_display_price', models.IntegerField(null=True, blank=True)),
                ('price_adjustment', models.IntegerField(null=True, blank=True)),
                ('estimated_weight', models.IntegerField(null=True, blank=True)),
                ('artisan_notified_at', models.DateTimeField(null=True, blank=True)),
                ('artisan_confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('estimated_completion_date', models.DateTimeField(null=True, blank=True)),
                ('invoice_sent_at', models.DateTimeField(null=True, blank=True)),
                ('invoice_paid_at', models.DateTimeField(null=True, blank=True)),
                ('progress_updated_at', models.DateTimeField(null=True, blank=True)),
                ('progress', models.SmallIntegerField(default=0)),
                ('complete_at', models.DateTimeField(null=True, blank=True)),
                ('customer_confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('shipped_at', models.DateTimeField(null=True, blank=True)),
                ('canceled_at', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('base_product', models.ForeignKey(related_name='commissions', to='seller.Product', null=True)),
                ('customer', models.ForeignKey(related_name='commissions', to='public.Customer', null=True)),
                ('product', models.OneToOneField(related_name='commission', null=True, to='seller.Product')),
                ('requirement_images', models.ManyToManyField(to='seller.Image')),
            ],
        ),
    ]
