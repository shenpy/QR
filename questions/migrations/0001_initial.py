# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Question'
        db.create_table(u'questions_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('asker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'questions', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'questions_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('replyer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['questions.Question'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'questions', ['Answer'])

        # Adding model 'Vote'
        db.create_table(u'questions_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questions.Answer'])),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.User'])),
        ))
        db.send_create_signal(u'questions', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['answer', 'voter']
        db.create_unique(u'questions_vote', ['answer_id', 'voter_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['answer', 'voter']
        db.delete_unique(u'questions_vote', ['answer_id', 'voter_id'])

        # Deleting model 'Question'
        db.delete_table(u'questions_question')

        # Deleting model 'Answer'
        db.delete_table(u'questions_answer')

        # Deleting model 'Vote'
        db.delete_table(u'questions_vote')


    models = {
        u'questions.answer': {
            'Meta': {'object_name': 'Answer'},
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['questions.Question']"}),
            'replyer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'voters': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'voted'", 'symmetrical': 'False', 'through': u"orm['questions.Vote']", 'to': u"orm['users.User']"})
        },
        u'questions.question': {
            'Meta': {'object_name': 'Question'},
            'asker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'questions.vote': {
            'Meta': {'unique_together': "(('answer', 'voter'),)", 'object_name': 'Vote'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['questions.Answer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers'", 'symmetrical': 'False', 'db_table': "'user_relationship'", 'to': u"orm['users.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40', 'db_index': 'True'})
        }
    }

    complete_apps = ['questions']