# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Post'
        db.create_table(u'add_vid_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('video', self.gf('embed_video.fields.EmbedVideoField')(max_length=200)),
            ('details', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'add_vid', ['Post'])


    def backwards(self, orm):
        # Deleting model 'Post'
        db.delete_table(u'add_vid_post')


    models = {
        u'add_vid.post': {
            'Meta': {'object_name': 'Post'},
            'details': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['add_vid']