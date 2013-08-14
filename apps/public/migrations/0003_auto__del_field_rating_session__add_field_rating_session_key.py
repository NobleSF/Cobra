# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Rating.session'
        db.delete_column('public_rating', 'session')

        # Adding field 'Rating.session_key'
        db.add_column('public_rating', 'session_key',
                      self.gf('django.db.models.fields.CharField')(default=None, unique=True, max_length=32),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Rating.session'
        raise RuntimeError("Cannot reverse this migration. 'Rating.session' and its values cannot be restored.")
        # Deleting field 'Rating.session_key'
        db.delete_column('public_rating', 'session_key')


    models = {
        'admin.account': {
            'Meta': {'object_name': 'Account'},
            'bank_account': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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
        'public.cart': {
            'Meta': {'object_name': 'Cart'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'checked_out': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'wepay_checkout_id': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'public.item': {
            'Meta': {'object_name': 'Item'},
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['public.Cart']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Product']"})
        },
        'public.order': {
            'Meta': {'object_name': 'Order'},
            'anou_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'cart': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['public.Cart']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount_charge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'discount_reason': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Product']", 'symmetrical': 'False'}),
            'products_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'receipt': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'received_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'returned_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reviewed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'seller_confirmed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'seller_notified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'seller_paid_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'seller_paid_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipped_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'shipping_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'shipping_option': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.ShippingOption']", 'null': 'True', 'blank': 'True'}),
            'shipping_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'total_charge': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'}),
            'tracking_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'public.rating': {
            'Meta': {'object_name': 'Rating'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Product']"}),
            'session_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.RatingSubject']"}),
            'value': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'public.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'public.visitor': {
            'Meta': {'object_name': 'Visitor'},
            'carts': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['public.Cart']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sessions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sessions.Session']", 'symmetrical': 'False'})
        },
        'seller.asset': {
            'Meta': {'object_name': 'Asset'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['admin.Category']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ilk': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.product': {
            'Meta': {'object_name': 'Product'},
            'active_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assets': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Asset']", 'symmetrical': 'False'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Color']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deactive_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'shipping_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.ShippingOption']", 'symmetrical': 'False'}),
            'sold_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'seller.seller': {
            'Meta': {'object_name': 'Seller'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Account']"}),
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'coordinates': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Currency']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.shippingoption': {
            'Meta': {'object_name': 'ShippingOption'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'sessions.session': {
            'Meta': {'object_name': 'Session', 'db_table': "'django_session'"},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'session_data': ('django.db.models.fields.TextField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'})
        }
    }

    complete_apps = ['public']