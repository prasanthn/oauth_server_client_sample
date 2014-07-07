# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccessInfo'
        db.create_table(u'oauth2_client_accessinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('access_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('token_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('expires_in', self.gf('django.db.models.fields.PositiveIntegerField')(max_length=255)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('scopes', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'oauth2_client', ['AccessInfo'])


    def backwards(self, orm):
        # Deleting model 'AccessInfo'
        db.delete_table(u'oauth2_client_accessinfo')


    models = {
        u'oauth2_client.accessinfo': {
            'Meta': {'object_name': 'AccessInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_in': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scopes': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'service': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'token_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['oauth2_client']