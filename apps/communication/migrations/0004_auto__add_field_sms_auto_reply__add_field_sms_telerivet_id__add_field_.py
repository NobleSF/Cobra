# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SMS.auto_reply'
        db.add_column('communication_sms', 'auto_reply',
                      self.gf('django.db.models.fields.CharField')(max_length=160, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SMS.telerivet_id'
        db.add_column('communication_sms', 'telerivet_id',
                      self.gf('django.db.models.fields.CharField')(default='1234567890123456789012345678901234', max_length=34),
                      keep_default=False)

        # Adding field 'SMS.updated_at'
        db.add_column('communication_sms', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 6, 18, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'SMS.status'
        db.alter_column('communication_sms', 'status', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

    def backwards(self, orm):
        # Deleting field 'SMS.auto_reply'
        db.delete_column('communication_sms', 'auto_reply')

        # Deleting field 'SMS.telerivet_id'
        db.delete_column('communication_sms', 'telerivet_id')

        # Deleting field 'SMS.updated_at'
        db.delete_column('communication_sms', 'updated_at')


        # Changing field 'SMS.status'
        db.alter_column('communication_sms', 'status', self.gf('django.db.models.fields.CharField')(default=None, max_length=15))

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
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'telerivet_id': ('django.db.models.fields.CharField', [], {'max_length': '34'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['communication']