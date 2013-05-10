# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Email.message'
        db.delete_column('communication_email', 'message')

        # Adding field 'Email.html_body'
        db.add_column('communication_email', 'html_body',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Email.text_body'
        db.add_column('communication_email', 'text_body',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Email.bcc_address'
        db.alter_column('communication_email', 'bcc_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Email.cc_address'
        db.alter_column('communication_email', 'cc_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Email.attachment'
        db.alter_column('communication_email', 'attachment', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Email.message'
        raise RuntimeError("Cannot reverse this migration. 'Email.message' and its values cannot be restored.")
        # Deleting field 'Email.html_body'
        db.delete_column('communication_email', 'html_body')

        # Deleting field 'Email.text_body'
        db.delete_column('communication_email', 'text_body')


        # User chose to not deal with backwards NULL issues for 'Email.bcc_address'
        raise RuntimeError("Cannot reverse this migration. 'Email.bcc_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Email.cc_address'
        raise RuntimeError("Cannot reverse this migration. 'Email.cc_address' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Email.attachment'
        raise RuntimeError("Cannot reverse this migration. 'Email.attachment' and its values cannot be restored.")

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
            'to_number': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['communication']