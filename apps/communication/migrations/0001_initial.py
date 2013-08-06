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
            ('cc_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('bcc_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('html_body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_body', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('attachment', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('communication', ['Email'])

        # Adding model 'SMS'
        db.create_table('communication_sms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('to_number', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('auto_reply', self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True)),
            ('telerivet_id', self.gf('django.db.models.fields.CharField')(max_length=34)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
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
            'attachment': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'bcc_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'cc_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'html_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'text_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'to_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        'communication.sms': {
            'Meta': {'object_name': 'SMS'},
            'auto_reply': ('django.db.models.fields.CharField', [], {'max_length': '160', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'telerivet_id': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['communication']