# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActivityLog'
        db.create_table(u'network_activitylog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('mac', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'network', ['ActivityLog'])


    def backwards(self, orm):
        # Deleting model 'ActivityLog'
        db.delete_table(u'network_activitylog')


    models = {
        u'network.activitylog': {
            'Meta': {'object_name': 'ActivityLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mac': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['network']