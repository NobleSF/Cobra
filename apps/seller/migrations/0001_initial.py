# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ilk', models.CharField(max_length=10)),
                ('rank', models.SmallIntegerField()),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('name_ol', models.CharField(max_length=50, null=True, blank=True)),
                ('description_ol', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='admin.Category', null=True, blank=True)),
            ],
            options={
                'ordering': ['rank', 'created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CustomOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.TextField(null=True, blank=True)),
                ('customer_email', models.TextField(null=True, blank=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('estimated_completion_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.SmallIntegerField()),
                ('is_progress', models.BooleanField(default=False)),
                ('original', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['product', 'rank'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.SmallIntegerField(null=True, blank=True)),
                ('height', models.SmallIntegerField(null=True, blank=True)),
                ('length', models.SmallIntegerField(null=True, blank=True)),
                ('weight', models.SmallIntegerField(null=True, blank=True)),
                ('price', models.SmallIntegerField(null=True, blank=True)),
                ('active_at', models.DateTimeField(null=True, blank=True)),
                ('deactive_at', models.DateTimeField(null=True, blank=True)),
                ('in_holding', models.BooleanField(default=False)),
                ('approved_at', models.DateTimeField(null=True, blank=True)),
                ('sold_at', models.DateTimeField(null=True, blank=True)),
                ('slug', models.CharField(max_length=150, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assets', models.ManyToManyField(to='seller.Asset')),
                ('colors', models.ManyToManyField(to='admin.Color')),
            ],
            options={
                'ordering': ['-sold_at', '-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bio', models.TextField(null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('coordinates', models.CharField(max_length=30, null=True, blank=True)),
                ('bio_ol', models.TextField(null=True, blank=True)),
                ('approved_at', models.DateTimeField(null=True, blank=True)),
                ('deactive_at', models.DateTimeField(null=True, blank=True)),
                ('slug', models.CharField(max_length=150, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(related_name='sellers', to='admin.Account')),
                ('country', models.ForeignKey(blank=True, to='admin.Country', null=True)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='seller.Image', null=True)),
                ('translated_by', models.ForeignKey(related_name='translator', blank=True, to='admin.Account', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShippingOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('country', models.ForeignKey(to='admin.Country')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='seller.Image', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public_id', models.CharField(unique=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('complete_at', models.DateTimeField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(to='seller.Seller'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='shipping_options',
            field=models.ManyToManyField(to='seller.ShippingOption'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(related_name='photos', to='seller.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='photo',
            unique_together=set([('product', 'rank')]),
        ),
        migrations.AddField(
            model_name='customorder',
            name='base_product',
            field=models.ForeignKey(related_name='custom_orders', to='seller.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customorder',
            name='custom_product',
            field=models.OneToOneField(to='seller.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='seller.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='seller',
            field=models.ForeignKey(to='seller.Seller'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='asset',
            unique_together=set([('seller', 'ilk', 'rank')]),
        ),
    ]
