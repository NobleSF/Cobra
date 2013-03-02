# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Order.shipping_option'
        db.alter_column('public_order', 'shipping_option_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.ShippingOption']))

    def backwards(self, orm):

        # Changing field 'Order.shipping_option'
        db.alter_column('public_order', 'shipping_option_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.ShippingOption']))

    models = {
        'admin.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'product': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Product']", 'symmetrical': 'False'}),
            'products_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'receipt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'received_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'shipped_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
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
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Category']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'seller.product': {
            'Meta': {'object_name': 'Product'},
            'asset': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Asset']", 'symmetrical': 'False'}),
            'color': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Color']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'shipping_option': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.ShippingOption']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'seller.seller': {
            'Meta': {'object_name': 'Seller'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Account']"}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Currency']"}),
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