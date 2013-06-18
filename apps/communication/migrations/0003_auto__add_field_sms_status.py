# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SMS.status'
        db.add_column('communication_sms', 'status',
                      self.gf('django.db.models.fields.CharField')(default='undefined', max_length=15),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SMS.status'
        db.delete_column('communication_sms', 'status')


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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['communication']