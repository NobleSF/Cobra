# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Colors'
        db.delete_table('admin_colors')

        # Deleting model 'Image'
        db.delete_table('admin_image')

        # Deleting model 'Order'
        db.delete_table('admin_order')

        # Removing M2M table for field product on 'Order'
        db.delete_table('admin_order_product')

        # Adding model 'RatingSubject'
        db.create_table('admin_ratingsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('admin', ['RatingSubject'])

        # Adding model 'Color'
        db.create_table('admin_color', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('admin', ['Color'])

        # Adding model 'Category'
        db.create_table('admin_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('admin', ['Category'])

        # Deleting field 'ShippingOption.image'
        db.delete_column('admin_shippingoption', 'image_id')


    def backwards(self, orm):
        # Adding model 'Colors'
        db.create_table('admin_colors', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('admin', ['Colors'])

        # Adding model 'Image'
        db.create_table('admin_image', (
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('admin', ['Image'])

        # Adding model 'Order'
        db.create_table('admin_order', (
            ('discount_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('receipt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('shipping_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('shipping_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('shipping_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('discount_reason', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_shipped', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shipped_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('received_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('is_seller_notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_arrived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_seller_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('anou_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('shipping_option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.ShippingOption'])),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Account'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('products_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('shipping_address', self.gf('django.db.models.fields.TextField')()),
            ('total_charge', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_artisan_paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('admin', ['Order'])

        # Adding M2M table for field product on 'Order'
        db.create_table('admin_order_product', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm['admin.order'], null=False)),
            ('product', models.ForeignKey(orm['seller.product'], null=False))
        ))
        db.create_unique('admin_order_product', ['order_id', 'product_id'])

        # Deleting model 'RatingSubject'
        db.delete_table('admin_ratingsubject')

        # Deleting model 'Color'
        db.delete_table('admin_color')

        # Deleting model 'Category'
        db.delete_table('admin_category')


        # User chose to not deal with backwards NULL issues for 'ShippingOption.image'
        raise RuntimeError("Cannot reverse this migration. 'ShippingOption.image' and its values cannot be restored.")

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
        'admin.shippingoption': {
            'Meta': {'object_name': 'ShippingOption'},
            'cost_formula': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['admin']