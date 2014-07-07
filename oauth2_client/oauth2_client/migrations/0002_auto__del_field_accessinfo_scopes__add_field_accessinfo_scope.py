# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AccessInfo.scopes'
        db.delete_column(u'oauth2_client_accessinfo', 'scopes')

        # Adding field 'AccessInfo.scope'
        db.add_column(u'oauth2_client_accessinfo', 'scope',
                      self.gf('django.db.models.fields.CharField')(default='date_joined', max_length=500),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'AccessInfo.scopes'
        db.add_column(u'oauth2_client_accessinfo', 'scopes',
                      self.gf('django.db.models.fields.CharField')(default='date_joined', max_length=500),
                      keep_default=False)

        # Deleting field 'AccessInfo.scope'
        db.delete_column(u'oauth2_client_accessinfo', 'scope')


    models = {
        u'oauth2_client.accessinfo': {
            'Meta': {'object_name': 'AccessInfo'},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_in': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'scope': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'service': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'token_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['oauth2_client']