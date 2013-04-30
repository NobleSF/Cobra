# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table('public_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Account'])),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('products_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('shipping_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('anou_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('discount_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('discount_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('total_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('receipt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shipping_address', self.gf('django.db.models.fields.TextField')()),
            ('shipping_option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.ShippingOption'])),
            ('shipping_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('shipping_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('shipped_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('received_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_seller_notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_seller_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_shipped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_arrived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_artisan_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('public', ['Order'])

        # Adding M2M table for field products on 'Order'
        db.create_table('public_order_products', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['public.order'], null=False)),
            ('product', models.ForeignKey(orm['seller.product'], null=False))
        ))
        db.create_unique('public_order_products', ['order_id', 'product_id'])

        # Adding model 'Rating'
        db.create_table('public_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Account'])),
            ('product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Product'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.RatingSubject'])),
            ('value', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('public', ['Rating'])

        # Adding model 'CustomerActivity'
        db.create_table('public_customeractivity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Product'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('public', ['CustomerActivity'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table('public_order')

        # Removing M2M table for field products on 'Order'
        db.delete_table('public_order_products')

        # Deleting model 'Rating'
        db.delete_table('public_rating')

        # Deleting model 'CustomerActivity'
        db.delete_table('public_customeractivity')


    models = {
        'admin.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'admin.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'admin.color': {
            'Meta': {'object_name': 'Color'},
            'hex_value': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'admin.country': {
            'Meta': {'object_name': 'Country'},
            'calling_code': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Currency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'admin.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'exchange_rate_to_USD': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'admin.ratingsubject': {
            'Meta': {'object_name': 'RatingSubject'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'public.customeractivity': {
            'Meta': {'object_name': 'CustomerActivity'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Product']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'public.order': {
            'Meta': {'object_name': 'Order'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Account']"}),
            'anou_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'discount_reason': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_arrived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_artisan_paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seller_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_seller_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_shipped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Product']", 'symmetrical': 'False'}),
            'products_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'receipt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'received_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'shipped_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_address': ('django.db.models.fields.TextField', [], {}),
            'shipping_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'shipping_option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.ShippingOption']"}),
            'shipping_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'public.rating': {
            'Meta': {'object_name': 'Rating'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Account']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Product']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.RatingSubject']"}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'seller.asset': {
            'Meta': {'object_name': 'Asset'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['admin.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilk': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'pinky': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'thumb': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.product': {
            'Meta': {'object_name': 'Product'},
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Asset']", 'symmetrical': 'False'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Color']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'shipping_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.ShippingOption']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'seller.seller': {
            'Meta': {'object_name': 'Seller'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Account']"}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Currency']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.shippingoption': {
            'Meta': {'object_name': 'ShippingOption'},
            'cost_formula': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['public']