# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('admin', '0001_initial'),
        ('public', '0003_cart_checkout_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_id', models.CharField(max_length=15, null=True, blank=True)),
                ('checkout_id', models.CharField(max_length=35, null=True, blank=True)),
                ('checkout_data', jsonfield.fields.JSONField(null=True, blank=True)),
                ('total_charge', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('total_discount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('total_paid', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('total_refunded', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('receipt', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.OneToOneField(related_name='checkout', to='public.Cart')),
                ('currency', models.ForeignKey(blank=True, to='admin.Currency', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(related_name='orders', blank=True, to='seller.Product', null=True),
            preserve_default=True,
        ),
    ]
