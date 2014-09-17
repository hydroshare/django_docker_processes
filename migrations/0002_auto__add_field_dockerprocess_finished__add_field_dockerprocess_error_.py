# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DockerProcess.finished'
        db.add_column(u'django_docker_processes_dockerprocess', 'finished',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'DockerProcess.error'
        db.add_column(u'django_docker_processes_dockerprocess', 'error',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'DockerProcess.container_id'
        db.alter_column(u'django_docker_processes_dockerprocess', 'container_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True))

    def backwards(self, orm):
        # Deleting field 'DockerProcess.finished'
        db.delete_column(u'django_docker_processes_dockerprocess', 'finished')

        # Deleting field 'DockerProcess.error'
        db.delete_column(u'django_docker_processes_dockerprocess', 'error')


        # User chose to not deal with backwards NULL issues for 'DockerProcess.container_id'
        raise RuntimeError("Cannot reverse this migration. 'DockerProcess.container_id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DockerProcess.container_id'
        db.alter_column(u'django_docker_processes_dockerprocess', 'container_id', self.gf('django.db.models.fields.CharField')(max_length=128))

    models = {
        u'django_docker_processes.containeroverrides': {
            'Meta': {'object_name': 'ContainerOverrides'},
            'command': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cpu_shares': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'dns': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'docker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'entrypoint': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lxc_conf': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'}),
            'memory_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'net': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'privileged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'}),
            'working_dir': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'})
        },
        u'django_docker_processes.dockerenvvar': {
            'Meta': {'object_name': 'DockerEnvVar'},
            'docker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'django_docker_processes.dockerlink': {
            'Meta': {'object_name': 'DockerLink'},
            'docker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'docker_profile_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile_link_to'", 'to': u"orm['django_docker_processes.DockerProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'django_docker_processes.dockerport': {
            'Meta': {'object_name': 'DockerPort'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            'docker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_docker_processes.dockerprocess': {
            'Meta': {'object_name': 'DockerProcess'},
            'container_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logs': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'a2f4909e-682a-4e99-b844-7298c6bf6ad8'", 'unique': 'True', 'max_length': '128', 'db_index': 'True'})
        },
        u'django_docker_processes.dockerprofile': {
            'Meta': {'object_name': 'DockerProfile'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'commit_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'git_password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '16384'}),
            'git_use_submodules': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'git_username': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024', 'db_index': 'True'})
        },
        u'django_docker_processes.dockervolume': {
            'Meta': {'object_name': 'DockerVolume'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            'docker_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readonly': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'django_docker_processes.overrideenvvar': {
            'Meta': {'object_name': 'OverrideEnvVar'},
            'container_overrides': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.ContainerOverrides']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        u'django_docker_processes.overridelink': {
            'Meta': {'object_name': 'OverrideLink'},
            'container_overrides': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.ContainerOverrides']"}),
            'docker_profile_from': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'django_docker_processes.overrideport': {
            'Meta': {'object_name': 'OverridePort'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            'container_overrides': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.ContainerOverrides']"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'django_docker_processes.overridevolume': {
            'Meta': {'object_name': 'OverrideVolume'},
            'container': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            'container_overrides': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.ContainerOverrides']"}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '65536'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['django_docker_processes']