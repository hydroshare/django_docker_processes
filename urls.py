from django.conf.urls import patterns, url
from django_docker_processes import views

urlpatterns = patterns('',
    url(r'^process_aborted/(?P<profile_name>[^/]+)/(?P<token>[A-z0-9]+)/$', views.process_aborted, name='docker-process-aborted'),
    url(r'^process_finished/(?P<profile_name>[^/]+)/(?P<token>[A-z0-9]+)/$', views.process_finished, name='docker-process-finished'),
)

