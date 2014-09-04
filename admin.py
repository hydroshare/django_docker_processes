from django.contrib import admin
from . import models

class DockerLinkInline(admin.TabularInline):
    model = models.DockerLink
    fk_name = 'docker_profile'
    extra = 1

class DockerEnvVarInline(admin.TabularInline):
    model = models.DockerEnvVar

class DockerPortInline(admin.TabularInline):
    model = models.DockerPort

class DockerVolumeInline(admin.TabularInline):
    model = models.DockerVolume

class DockerProfileAdmin(admin.ModelAdmin):
    inlines = [DockerLinkInline, DockerEnvVarInline, DockerPortInline, DockerVolumeInline]

# now do the overrides

class OverrideLinkInline(admin.TabularInline):
    model = models.OverrideLink

class OverrideEnvVarInline(admin.TabularInline):
    model = models.OverrideEnvVar

class OverridePortInline(admin.TabularInline):
    model = models.OverridePort

class OverrideVolumeInline(admin.TabularInline):
    model = models.OverrideVolume

class ContainerOverridesAdmin(admin.ModelAdmin):
    inlines = [OverrideLinkInline, OverrideEnvVarInline, OverridePortInline, OverrideVolumeInline]

admin.site.register(models.DockerProfile, DockerProfileAdmin)
admin.site.register(models.ContainerOverrides, ContainerOverridesAdmin)
