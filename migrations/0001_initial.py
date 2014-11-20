# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django_docker_processes.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContainerOverrides',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('command', models.TextField(null=True, blank=True)),
                ('working_dir', models.CharField(max_length=65536, null=True, blank=True)),
                ('user', models.CharField(max_length=65536, null=True, blank=True)),
                ('entrypoint', models.CharField(max_length=65536, null=True, blank=True)),
                ('privileged', models.BooleanField(default=False)),
                ('lxc_conf', models.CharField(max_length=65536, null=True, blank=True)),
                ('memory_limit', models.IntegerField(default=0, help_text=b'megabytes')),
                ('cpu_shares', models.IntegerField(help_text=b'CPU Shares', null=True, blank=True)),
                ('dns', jsonfield.fields.JSONField(help_text=b'JSON list of alternate DNS servers', null=True, blank=True)),
                ('net', models.CharField(blank=True, max_length=8, null=True, help_text=b'Network settings - leave blank for default behavior', choices=[(b'bridge', b'bridge'), (b'none', b'none'), (b'host', b'host')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerEnvVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_name', models.CharField(max_length=256)),
                ('docker_overrides', models.ForeignKey(blank=True, to='django_docker_processes.ContainerOverrides', help_text=b'Overrides for the container to run', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerPort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=65536)),
                ('container', models.CharField(max_length=65536)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('container_id', models.CharField(max_length=128, null=True, blank=True)),
                ('token', models.CharField(default=django_docker_processes.models.docker_process_token, unique=True, max_length=128, db_index=True)),
                ('logs', models.TextField(null=True, blank=True)),
                ('finished', models.BooleanField(default=False)),
                ('error', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=1024, db_index=True)),
                ('git_repository', models.CharField(max_length=16384)),
                ('git_use_submodules', models.BooleanField(default=False)),
                ('git_username', models.CharField(max_length=256, null=True, blank=True)),
                ('git_password', models.CharField(max_length=64, null=True, blank=True)),
                ('commit_id', models.CharField(max_length=64, null=True, blank=True)),
                ('branch', models.CharField(default=b'master', max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DockerVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=65536, null=True, blank=True)),
                ('container', models.CharField(max_length=65536)),
                ('readonly', models.BooleanField(default=False)),
                ('docker_profile', models.ForeignKey(to='django_docker_processes.DockerProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverrideEnvVar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1024)),
                ('value', models.TextField()),
                ('container_overrides', models.ForeignKey(to='django_docker_processes.ContainerOverrides')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverrideLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_name', models.CharField(max_length=256)),
                ('container_overrides', models.ForeignKey(to='django_docker_processes.ContainerOverrides')),
                ('docker_profile_from', models.ForeignKey(help_text=b'This container must be started and running for the target to run', to='django_docker_processes.DockerProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverridePort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=65536)),
                ('container', models.CharField(max_length=65536)),
                ('container_overrides', models.ForeignKey(to='django_docker_processes.ContainerOverrides')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OverrideVolume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=65536)),
                ('container', models.CharField(max_length=65536)),
                ('container_overrides', models.ForeignKey(to='django_docker_processes.ContainerOverrides')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dockerprocess',
            name='profile',
            field=models.ForeignKey(to='django_docker_processes.DockerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dockerprocess',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dockerport',
            name='docker_profile',
            field=models.ForeignKey(to='django_docker_processes.DockerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dockerlink',
            name='docker_profile',
            field=models.ForeignKey(help_text=b'This is the "target" container.  It will receive information about\nthe "from" container as an environment var', to='django_docker_processes.DockerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dockerlink',
            name='docker_profile_from',
            field=models.ForeignKey(related_name='profile_link_to', to='django_docker_processes.DockerProfile', help_text=b'This container must be started and running for the target to run'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dockerenvvar',
            name='docker_profile',
            field=models.ForeignKey(to='django_docker_processes.DockerProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='containeroverrides',
            name='docker_profile',
            field=models.ForeignKey(to='django_docker_processes.DockerProfile'),
            preserve_default=True,
        ),
    ]
