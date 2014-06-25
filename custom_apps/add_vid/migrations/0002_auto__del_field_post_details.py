# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.details'
        db.delete_column(u'add_vid_post', 'details')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Post.details'
        raise RuntimeError("Cannot reverse this migration. 'Post.details' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Post.details'
        db.add_column(u'add_vid_post', 'details',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


    models = {
        u'add_vid.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video': ('embed_video.fields.EmbedVideoField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['add_vid']