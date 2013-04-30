# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Email'
        db.create_table('communication_email', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('to_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('cc_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('bcc_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('attachment', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('communication', ['Email'])

        # Adding model 'SMS'
        db.create_table('communication_sms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('to_number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('communication', ['SMS'])


    def backwards(self, orm):
        # Deleting model 'Email'
        db.delete_table('communication_email')

        # Deleting model 'SMS'
        db.delete_table('communication_sms')


    models = {
        'communication.email': {
            'Meta': {'object_name': 'Email'},
            'attachment': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'bcc_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'cc_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'to_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'communication.sms': {
            'Meta': {'object_name': 'SMS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['communication']