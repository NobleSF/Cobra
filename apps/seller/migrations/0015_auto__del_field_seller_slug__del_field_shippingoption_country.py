# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Seller.slug'
        db.delete_column(u'seller_seller', 'slug')

        # Deleting field 'ShippingOption.country'
        db.delete_column(u'seller_shippingoption', 'country_id')


    def backwards(self, orm):
        # Adding field 'Seller.slug'
        db.add_column(u'seller_seller', 'slug',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ShippingOption.country'
        raise RuntimeError("Cannot reverse this migration. 'ShippingOption.country' and its values cannot be restored.")

    models = {
        'admin.account': {
            'Meta': {'object_name': 'Account'},
            'admin_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'bank_account': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        'admin.category': {
            'Meta': {'ordering': "['ordering_name']", 'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ordering_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_categories'", 'null': 'True', 'to': "orm['admin.Category']"}),
            'plural_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'admin.color': {
            'Meta': {'ordering': "['id']", 'object_name': 'Color'},
            'hex_value': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'admin.country': {
            'Meta': {'object_name': 'Country'},
            'calling_code': ('django.db.models.fields.IntegerField', [], {}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Currency']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'admin.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'exchange_rate_to_USD': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.asset': {
            'Meta': {'ordering': "['rank', 'created_at']", 'unique_together': "(('seller', 'ilk', 'rank'),)", 'object_name': 'Asset'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['admin.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description_ol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilk': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_ol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.customorder': {
            'Meta': {'object_name': 'CustomOrder'},
            'base_product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'custom_orders'", 'null': 'True', 'to': "orm['seller.Product']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'custom_product': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['seller.Product']", 'unique': 'True'}),
            'customer_email': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_completion_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.photo': {
            'Meta': {'ordering': "['product', 'rank']", 'unique_together': "(('product', 'rank'),)", 'object_name': 'Photo'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'original': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': "orm['seller.Product']"}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.product': {
            'Meta': {'ordering': "['-sold_at', '-id']", 'object_name': 'Product'},
            'active_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Asset']", 'symmetrical': 'False'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Color']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactive_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_holding': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'products'", 'to': "orm['seller.Seller']"}),
            'shipping_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.ShippingOption']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'sold_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'seller.seller': {
            'Meta': {'object_name': 'Seller'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sellers'", 'to': "orm['admin.Account']"}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_ol': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactive_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'translated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'translator'", 'null': 'True', 'to': "orm['admin.Account']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.shippingoption': {
            'Meta': {'object_name': 'ShippingOption'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'seller.upload': {
            'Meta': {'object_name': 'Upload'},
            'complete_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['seller']