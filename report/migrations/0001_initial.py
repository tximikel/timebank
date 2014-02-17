# -*- coding: utf-8 -*-
import os 
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        SQLDIR = os.path.join(os.path.dirname(__file__),'..','sql')
        print "Sql directory: '%s'" % SQLDIR
        sqlfile = os.path.join(SQLDIR,'dbviews-mysql.sql')
        print "Sql file: '%s'" % sqlfile
        sql = open(sqlfile).read()
        print "Sql to execute: views: %s  lines: %s" % (sql.count('create or replace view'),  sql.count('\n'))
        db.execute_many(sql)
        #db.execute_many(sql, regex=r"(?mx) ([^';]* (?:'[^']*'[^';]*)*)", comment_regex=r"(?mx) (?:^\s*$)|(?:--.*$)") #remove comments        
        print "Sql executed!"
        #pass

    def backwards(self, orm):
        pass

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'report.report': {
            'Meta': {'object_name': 'Report', 'managed': 'False'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'report.serv_transferences': {
            'Meta': {'object_name': 'Serv_transferences', 'db_table': "'vw_serv_transf'", 'managed': 'False'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serv.Area']", 'null': 'True', 'blank': 'True'}),
            'area_id': ('django.db.models.fields.IntegerField', [], {}),
            'area_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True',  'db_column':'id', 'editable':'False'}),
            #'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True',  'db_column':'user_id', 'editable':'False'}),
            'is_offer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'serv_desc': ('django.db.models.fields.TextField', [], {}),
            'serv_id': ('django.db.models.fields.IntegerField', [], {}),
            'transf_debtor': ('django.db.models.fields.FloatField', [], {}),
            'transf_debtor_sum': ('django.db.models.fields.FloatField', [], {}),
            'transf_payee': ('django.db.models.fields.FloatField', [], {}),
            'transf_payee_sum': ('django.db.models.fields.FloatField', [], {}),
            'transf_user': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'report.transf_balance_check': {
            'Meta': {'object_name': 'Transf_balance_check', 'db_table': "'vw_transf_balance_check'", 'managed': 'False'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['serv.Area']", 'null': 'True', 'blank': 'True'}),
            'area_id': ('django.db.models.fields.IntegerField', [], {}),
            'area_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'balance_check': ('django.db.models.fields.FloatField', [], {}),
            'balance_tot': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True',  'db_column':'id', 'editable':'False'}),
            #'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True',  'db_column':'user_id', 'editable':'False'}),            
            'transf_debtor': ('django.db.models.fields.FloatField', [], {}),
            'transf_payee': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'on_delete': 'models.DO_NOTHING', 'blank': 'True'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'serv.area': {
            'Meta': {'object_name': 'Area'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['report']
