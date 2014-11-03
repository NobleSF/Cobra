# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
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
                ('wepay_checkout_id', models.BigIntegerField(null=True, blank=True)),
                ('anou_checkout_id', models.CharField(max_length=15, null=True, blank=True)),
                ('checked_out', models.BooleanField(default=False)),
                ('receipt', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cart', models.ForeignKey(to='public.Cart')),
                ('product', models.ForeignKey(to='seller.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('products_charge', models.DecimalField(max_digits=8, decimal_places=2)),
                ('anou_charge', models.DecimalField(max_digits=8, decimal_places=2)),
                ('shipping_charge', models.DecimalField(max_digits=8, decimal_places=2)),
                ('total_charge', models.DecimalField(max_digits=8, decimal_places=2)),
                ('shipping_weight', models.FloatField(null=True, blank=True)),
                ('shipping_cost', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('tracking_number', models.CharField(max_length=50, null=True, blank=True)),
                ('seller_paid_amount', models.DecimalField(null=True, max_digits=8, decimal_places=2, blank=True)),
                ('seller_notified_at', models.DateTimeField(null=True, blank=True)),
                ('seller_confirmed_at', models.DateTimeField(null=True, blank=True)),
                ('shipped_at', models.DateTimeField(null=True, blank=True)),
                ('received_at', models.DateTimeField(null=True, blank=True)),
                ('reviewed_at', models.DateTimeField(null=True, blank=True)),
                ('seller_paid_at', models.DateTimeField(null=True, blank=True)),
                ('returned_at', models.DateTimeField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(related_name='orders', to='public.Cart')),
                ('products', models.ManyToManyField(to='seller.Product')),
                ('seller_paid_receipt', models.ForeignKey(blank=True, to='seller.Image', null=True)),
                ('shipping_option', models.ForeignKey(blank=True, to='seller.ShippingOption', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photography', models.DecimalField(default=b'0.50', max_digits=3, decimal_places=2)),
                ('price', models.DecimalField(default=b'0.50', max_digits=3, decimal_places=2)),
                ('appeal', models.DecimalField(default=b'0.50', max_digits=3, decimal_places=2)),
                ('new_product', models.DecimalField(default=b'1.00', max_digits=3, decimal_places=2)),
                ('new_store', models.DecimalField(default=b'1.00', max_digits=3, decimal_places=2)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(to='seller.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(max_length=32)),
                ('value', models.SmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(to='seller.Product')),
                ('subject', models.ForeignKey(to='admin.RatingSubject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='cart',
            name='promotions',
            field=models.ManyToManyField(to='public.Promotion'),
            preserve_default=True,
        ),
    ]
