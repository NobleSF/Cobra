# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Tool'
        db.delete_table('seller_tool')

        # Deleting model 'Artisan'
        db.delete_table('seller_artisan')

        # Deleting model 'ProductType'
        db.delete_table('seller_producttype')

        # Deleting model 'Material'
        db.delete_table('seller_material')

        # Adding model 'Category'
        db.create_table('seller_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('seller', ['Category'])

        # Adding model 'Asset'
        db.create_table('seller_asset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Seller'])),
            ('rank', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Image'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('seller', ['Asset'])

        # Adding M2M table for field category on 'Asset'
        db.create_table('seller_asset_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('asset', models.ForeignKey(orm['seller.asset'], null=False)),
            ('category', models.ForeignKey(orm['seller.category'], null=False))
        ))
        db.create_unique('seller_asset_category', ['asset_id', 'category_id'])

        # Deleting field 'Product.product_type'
        db.delete_column('seller_product', 'product_type_id')

        # Removing M2M table for field artisans on 'Product'
        db.delete_table('seller_product_artisans')

        # Removing M2M table for field materials on 'Product'
        db.delete_table('seller_product_materials')

        # Removing M2M table for field tools on 'Product'
        db.delete_table('seller_product_tools')

        # Adding M2M table for field asset on 'Product'
        db.create_table('seller_product_asset', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['seller.product'], null=False)),
            ('asset', models.ForeignKey(orm['seller.asset'], null=False))
        ))
        db.create_unique('seller_product_asset', ['product_id', 'asset_id'])


        # Changing field 'Product.weight'
        db.alter_column('seller_product', 'weight', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'Product.price'
        db.alter_column('seller_product', 'price', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'Product.height'
        db.alter_column('seller_product', 'height', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'Product.width'
        db.alter_column('seller_product', 'width', self.gf('django.db.models.fields.SmallIntegerField')(null=True))

        # Changing field 'Product.length'
        db.alter_column('seller_product', 'length', self.gf('django.db.models.fields.SmallIntegerField')(null=True))
        # Deleting field 'Photo.order'
        db.delete_column('seller_photo', 'order')

        # Deleting field 'Photo.file'
        db.delete_column('seller_photo', 'file')

        # Adding field 'Photo.rank'
        db.add_column('seller_photo', 'rank',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Photo.url'
        db.add_column('seller_photo', 'url',
                      self.gf('django.db.models.fields.URLField')(default='http://www.theanou.com', max_length=200),
                      keep_default=False)

        # Adding field 'Photo.thumbnail'
        db.add_column('seller_photo', 'thumbnail',
                      self.gf('django.db.models.fields.CharField')(default='http://www.theanou.com', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Tool'
        db.create_table('seller_tool', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Image'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Seller'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('seller', ['Tool'])

        # Adding model 'Artisan'
        db.create_table('seller_artisan', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Image'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Seller'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('seller', ['Artisan'])

        # Adding model 'ProductType'
        db.create_table('seller_producttype', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Image'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Seller'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('seller', ['ProductType'])

        # Adding model 'Material'
        db.create_table('seller_material', (
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['admin.Image'])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['seller.Seller'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('seller', ['Material'])

        # Deleting model 'Category'
        db.delete_table('seller_category')

        # Deleting model 'Asset'
        db.delete_table('seller_asset')

        # Removing M2M table for field category on 'Asset'
        db.delete_table('seller_asset_category')


        # User chose to not deal with backwards NULL issues for 'Product.product_type'
        raise RuntimeError("Cannot reverse this migration. 'Product.product_type' and its values cannot be restored.")
        # Adding M2M table for field artisans on 'Product'
        db.create_table('seller_product_artisans', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['seller.product'], null=False)),
            ('artisan', models.ForeignKey(orm['seller.artisan'], null=False))
        ))
        db.create_unique('seller_product_artisans', ['product_id', 'artisan_id'])

        # Adding M2M table for field materials on 'Product'
        db.create_table('seller_product_materials', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['seller.product'], null=False)),
            ('material', models.ForeignKey(orm['seller.material'], null=False))
        ))
        db.create_unique('seller_product_materials', ['product_id', 'material_id'])

        # Adding M2M table for field tools on 'Product'
        db.create_table('seller_product_tools', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['seller.product'], null=False)),
            ('tool', models.ForeignKey(orm['seller.tool'], null=False))
        ))
        db.create_unique('seller_product_tools', ['product_id', 'tool_id'])

        # Removing M2M table for field asset on 'Product'
        db.delete_table('seller_product_asset')


        # Changing field 'Product.weight'
        db.alter_column('seller_product', 'weight', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product.price'
        db.alter_column('seller_product', 'price', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product.height'
        db.alter_column('seller_product', 'height', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product.width'
        db.alter_column('seller_product', 'width', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Product.length'
        db.alter_column('seller_product', 'length', self.gf('django.db.models.fields.IntegerField')(null=True))

        # User chose to not deal with backwards NULL issues for 'Photo.order'
        raise RuntimeError("Cannot reverse this migration. 'Photo.order' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Photo.file'
        raise RuntimeError("Cannot reverse this migration. 'Photo.file' and its values cannot be restored.")
        # Deleting field 'Photo.rank'
        db.delete_column('seller_photo', 'rank')

        # Deleting field 'Photo.url'
        db.delete_column('seller_photo', 'url')

        # Deleting field 'Photo.thumbnail'
        db.delete_column('seller_photo', 'thumbnail')


    models = {
        'admin.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'admin.colors': {
            'Meta': {'object_name': 'Colors'},
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
        'admin.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'admin.shippingoption': {
            'Meta': {'object_name': 'ShippingOption'},
            'cost_formula': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'seller.asset': {
            'Meta': {'object_name': 'Asset'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Category']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['admin.Image']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'seller.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'seller.photo': {
            'Meta': {'object_name': 'Photo'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Product']"}),
            'rank': ('django.db.models.fields.SmallIntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'seller.product': {
            'Meta': {'object_name': 'Product'},
            'asset': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['seller.Asset']", 'symmetrical': 'False'}),
            'colors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.Colors']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'length': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['seller.Seller']"}),
            'shipping_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['admin.ShippingOption']", 'symmetrical': 'False'}),
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
            'email': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['seller']