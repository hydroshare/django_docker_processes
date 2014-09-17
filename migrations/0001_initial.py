# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DockerProfile'
        db.create_table(u'django_docker_processes_dockerprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024, db_index=True)),
            ('git_repository', self.gf('django.db.models.fields.CharField')(max_length=16384)),
            ('git_use_submodules', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('git_username', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('git_password', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('commit_id', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('branch', self.gf('django.db.models.fields.CharField')(default='master', max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerProfile'])

        # Adding model 'ContainerOverrides'
        db.create_table(u'django_docker_processes_containeroverrides', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('command', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('working_dir', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
            ('entrypoint', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
            ('privileged', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lxc_conf', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
            ('memory_limit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cpu_shares', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dns', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('net', self.gf('django.db.models.fields.CharField')(max_length=8, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_docker_processes', ['ContainerOverrides'])

        # Adding model 'OverrideEnvVar'
        db.create_table(u'django_docker_processes_overrideenvvar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container_overrides', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.ContainerOverrides'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'django_docker_processes', ['OverrideEnvVar'])

        # Adding model 'OverrideVolume'
        db.create_table(u'django_docker_processes_overridevolume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container_overrides', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.ContainerOverrides'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=65536)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=65536)),
        ))
        db.send_create_signal(u'django_docker_processes', ['OverrideVolume'])

        # Adding model 'OverrideLink'
        db.create_table(u'django_docker_processes_overridelink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container_overrides', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.ContainerOverrides'])),
            ('link_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('docker_profile_from', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
        ))
        db.send_create_signal(u'django_docker_processes', ['OverrideLink'])

        # Adding model 'OverridePort'
        db.create_table(u'django_docker_processes_overrideport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('container_overrides', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.ContainerOverrides'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=65536)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=65536)),
        ))
        db.send_create_signal(u'django_docker_processes', ['OverridePort'])

        # Adding model 'DockerLink'
        db.create_table(u'django_docker_processes_dockerlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('link_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('docker_profile_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='profile_link_to', to=orm['django_docker_processes.DockerProfile'])),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerLink'])

        # Adding model 'DockerEnvVar'
        db.create_table(u'django_docker_processes_dockerenvvar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerEnvVar'])

        # Adding model 'DockerVolume'
        db.create_table(u'django_docker_processes_dockervolume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True, blank=True)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=65536)),
            ('readonly', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerVolume'])

        # Adding model 'DockerPort'
        db.create_table(u'django_docker_processes_dockerport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docker_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=65536)),
            ('container', self.gf('django.db.models.fields.CharField')(max_length=65536)),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerPort'])

        # Adding model 'DockerProcess'
        db.create_table(u'django_docker_processes_dockerprocess', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_docker_processes.DockerProfile'])),
            ('container_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('token', self.gf('django.db.models.fields.CharField')(default='e34620a5-cf14-4997-a0e7-3a48cf332ce4', unique=True, max_length=128, db_index=True)),
            ('logs', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'django_docker_processes', ['DockerProcess'])


    def backwards(self, orm):
        # Deleting model 'DockerProfile'
        db.delete_table(u'django_docker_processes_dockerprofile')

        # Deleting model 'ContainerOverrides'
        db.delete_table(u'django_docker_processes_containeroverrides')

        # Deleting model 'OverrideEnvVar'
        db.delete_table(u'django_docker_processes_overrideenvvar')

        # Deleting model 'OverrideVolume'
        db.delete_table(u'django_docker_processes_overridevolume')

        # Deleting model 'OverrideLink'
        db.delete_table(u'django_docker_processes_overridelink')

        # Deleting model 'OverridePort'
        db.delete_table(u'django_docker_processes_overrideport')

        # Deleting model 'DockerLink'
        db.delete_table(u'django_docker_processes_dockerlink')

        # Deleting model 'DockerEnvVar'
        db.delete_table(u'django_docker_processes_dockerenvvar')

        # Deleting model 'DockerVolume'
        db.delete_table(u'django_docker_processes_dockervolume')

        # Deleting model 'DockerPort'
        db.delete_table(u'django_docker_processes_dockerport')

        # Deleting model 'DockerProcess'
        db.delete_table(u'django_docker_processes_dockerprocess')


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
            'container_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logs': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_docker_processes.DockerProfile']"}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'dddda7c1-2f3e-4dad-b33e-04021d938b0a'", 'unique': 'True', 'max_length': '128', 'db_index': 'True'})
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