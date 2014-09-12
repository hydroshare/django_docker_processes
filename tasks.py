from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
import docker
import sh
from tempfile import mkdtemp
from celery import shared_task
from urllib import urlencode
from django_docker_processes import models
from .settings import DOCKER_URL, DOCKER_API_VERSION
import contextlib
import os

@contextlib.contextmanager
def cd(path):
   old_path = os.getcwd()
   os.chdir(path)
   try:
       yield
   finally:
       os.chdir(old_path)

dock = docker.Client(base_url=DOCKER_URL, version=DOCKER_API_VERSION)

@shared_task
def build_image(profile, clean=False, ignore_cache=False):
    """
    Builds a container on this host if it doesn't exist or cleans and rebuilds it

    :param profile:
    :param clean:
    :param ignore_cache:
    :return:
    """

    tmpd = mkdtemp(prefix='django_docker_processes_')

    with cd(tmpd):
        sh.git('clone', profile.git_repository, 'repo')

        with cd(tmpd + '/repo'):
            if profile.commit_id:
                sh.git('checkout', profile.commit_id)
            elif profile.branch:
                sh.git('checkout', profile.branch)

            if profile.git_use_submodules:
                sh.git('submodule','init')
                sh.git('submodule','update')

        result = dock.build(path=tmpd + '/repo', tag=profile.identifier, quiet=True, nocache=ignore_cache)
        for x in result:
            print x  # fixme this should use logger

    sh.rm('-rf', tmpd)
    return result

def create_container(profile, overrides=None, **kwargs):
    """
    Creates all containers from a profile, including links.

    :param profile: a DockerProfile object that describes how to build and run the container.
    :param overrides: A DockerfileOverrides object that changes the default behavior of the container.
    :param kwargs: Any further overrides as Docker run arguments.  These override both the profile and the overrides.

    Valid keyword args:

        - env : a dict of string key-value pairs that supply extra environment variables
        - ports : a dict of container:host string-string pairs that supply info on how to map ports (see docker for more docs on this)
        - volumes : a dict of name:directory or directory:directory pairs that supply info on binding volumes (see docker docs for more on this)
        - memory_limit : an integer in megabytes of the max memory allocated to the container
        - cpu_shares : see docker run docs
        - entrypoint : see docker run docs
        - user : see docker run docs
        - working_dir - see docker run docs
        - command - see docker run docs

    :return: the JSON description of the container from docker-py
    """

    print "keyword args: " + str(kwargs)
    
    # get the environment from the profile and construct it as a dict.
    environment = {e.name: e.value for e in profile.dockerenvvar_set.all()}
    # grab extra environment vars from keyword args
    specific_environment = kwargs.get('env', {})

    # get the ports from the environment and construct a port set
    ports = {e.container for e in profile.dockerport_set.all()}
    # get the ports from the keyword args and add to the set
    specific_ports = kwargs.get('ports', set())

    # get the volumes from the environment and construct them as a set
    volumes = {e.container for e in profile.dockervolume_set.all()}
    # get the volumes from the keyword args and add to the set
    specific_volumes = kwargs.get('volumes', set())

    # construct the container itself.  If there are overrides, apply them first.
    # After any possible overrides are applied add the keyword arguments to
    if not overrides:
        environment.update(specific_environment)
        ports = ports.union(specific_ports)
        volumes = volumes.union(specific_volumes)
        ports = list(ports)
        volumes = list(volumes)

        # memory limit handled specially because we're expecting megabytes, which needs a suffix
        mem_limit = 0 if 'memory_limit' not in kwargs else (str(kwargs['memory_limit']) + 'M')

        container = dock.create_container(
            profile.identifier,
            mem_limit=mem_limit,
            cpu_shares=kwargs.get('cpu_shares', None),
            entrypoint=kwargs.get('entrypoint', None),
            user=kwargs.get('user', None),
            working_dir=kwargs.get('working_dir', None),
            command=kwargs.get('command', None),
            environment=environment,
            ports=ports if len(ports) else None,
            volumes=volumes if len(volumes) else None
        )
    else:
        # apply overrides, then apply keyword args
        if overrides.overrideenvvar_set.exists():
            over_env = {e.name: e.value for e in  overrides.overrideenvvar_set.all()}
            environment.update(over_env)
        environment.update(specific_environment)

        # apply overrides, then apply keyword args
        if overrides.overrideport_set.exists():
            over_port = {e.container for e in  overrides.overrideport_set.all()}
            ports = ports.union(over_port)
        ports = ports.union(specific_ports)
        ports = list(ports)

        # memory limit handled specially because we're expecting megabytes, which needs a suffix
        mem_limit = (str(overrides.memory_limit)+'M') if overrides.memory_limit else 0
        mem_limit = mem_limit if 'memory_limit' not in kwargs else (str(kwargs['memory_limit']) + 'M')

        # apply overrides, then apply keyword args
        if overrides.overridevolume_set.exists():
            over_vol = {e.container for e in  overrides.overridevolume_set}
            volumes = volumes.union(over_vol)
        volumes = volumes.union(specific_volumes)
        volumes = list(volumes)

        container = dock.create_container(
            profile.identifier,
            mem_limit=mem_limit,
            cpu_shares=kwargs.get('cpu_shares', overrides.cpu_shares),
            entrypoint=kwargs.get('entrypoint', overrides.entrypoint),
            user=kwargs.get('user', overrides.user),
            working_dir=kwargs.get('working_dir', overrides.working_dir),
            command=kwargs.get('commmand', overrides.command),
            environment=environment,
            ports=ports if len(ports) else None,
            volumes=volumes if len(volumes) else None
        )

    return container

def start_container(profile, name, overrides=None, **kwargs):
    """
    Creates all containers from a profile, including links.

    :param profile: a DockerProfile object that describes how to build and run the container.
    :param overrides: A DockerfileOverrides object that changes the default behavior of the container.
    :param kwargs: Any further overrides as Docker run arguments.  These override both the profile and the overrides.

    valid keyword args are the same as in docker-py and docker:
        - env
        - ports
        - volumes
        - links
        - lxc_conf
        - privileged
        - dns
        - volumes_from
        - network_mode

    :return:
    """


    # get the environment from the profile and construct it as a dict.
    environment = {e.name: e.value for e in profile.dockerenvvar_set.all()}
    # grab extra environment vars from keyword args
    specific_environment = kwargs.get('env', {})

    # get the ports from the environment and construct a port set
    ports = {e.container: e.host for e in profile.dockerport_set.all()}
    # get the ports from the keyword args and add to the set
    specific_ports = kwargs.get('ports', {})

    # get the volumes from the environment and construct them as a set
    volumes = {e.container: e.host for e in profile.dockervolume_set.all()}
    # get the volumes from the keyword args and add to the set
    specific_volumes = kwargs.get('volumes', {})

    # get the links from the environment and construct them as a set
    links = {e.container: e.host for e in profile.dockerlink_set.all()}
    # get the links from the keyword args and add to the set
    specific_links = kwargs.get('links', {})

    # construct the container itself.  If there are overrides, apply them first.
    # After any possible overrides are applied add the keyword arguments to
    if not overrides:
        environment.update(specific_environment)
        ports.update(specific_ports)
        volumes.update(specific_volumes)
        links.update(specific_links)

        dock.start(
            name,
            lxc_conf=kwargs.get('lxc_conf', None),
            privileged=kwargs.get('privileged', None),
            dns=kwargs.get('dns', None),
            links=links,
            volumes_from=kwargs.get('volumes_from', None),
            network_mode=kwargs.get('network_mode', None),
            port_bindings=ports if len(ports) else None,
            binds=volumes if len(volumes) else None
        )
    else:
        # apply overrides, then apply keyword args
        if overrides.overrideenvvar_set.exists():
            over_env = {e.name: e.value for e in  overrides.overrideenvvar_set.all()}
            environment.update(over_env)
        environment.update(specific_environment)

        # apply overrides, then apply keyword args
        if overrides.overrideport_set.exists():
            over_port = {e.container:e.host for e in  overrides.overrideport_set.all()}
            ports.update(over_port)
        ports.update(specific_ports)

        # apply overrides, then apply keyword args
        if overrides.overridevolume_set.exists():
            over_vol = {e.container:e.host for e in  overrides.overridevolume_set.all()}
            volumes.update(over_vol)
        volumes.update(specific_volumes)

        if overrides.overridelink_set.exists():
            over_vol = {e.docker_profile_from: e.link_name for e in  overrides.overridelink_set.all()}
            volumes.update(over_vol)
        links.update(specific_links)

        dock.start(
            name,
            lxc_conf=kwargs.get('lxc_conf', overrides.lxc_conf),
            privileged=kwargs.get('privileged', overrides.privileged),
            dns=kwargs.get('dns', [d.strip() for d in overrides.dns.split(',')] if overrides.dns else None),
            links=links,
            volumes_from=kwargs.get('volumes_from', None),
            network_mode=kwargs.get('network_mode', None),
            port_bindings=ports if len(ports) else None,
            binds=volumes if len(volumes) else None
        )

@shared_task
def remove_image(profile):
    """

    :param profile:
    :return:
    """
    remove_stopped_containers.s()()
    dock.remove_image(profile.identifier)

def remove_container(container):
    """

    :param container:
    :return:
    """

    dock.remove_container(container)

@shared_task
def remove_stopped_containers():
    """
    Remove all stopped containers.  Broadcast task.

    :return:
    """

    all_containers = {i['Id'] for i in dock.containers(all=True)}
    running_containers = {i['Id'] for i in dock.containers(all=False)}
    dead_containers = all_containers.difference(running_containers)
    for c in dead_containers:
        dock.remove_container(c)


@shared_task
def run_process(profile, overrides=None, **kwargs):
    """
    This is the most common task you will want to use.

    Valid keyword args:

        - env : a dict of string key-value pairs that supply extra environment variables
        - ports : a dict of container:host string-string pairs that supply info on how to map ports (see docker for more docs on this)
        - volumes : a dict of name:directory or directory:directory pairs that supply info on binding volumes (see docker docs for more on this)
        - memory_limit : an integer in megabytes of the max memory allocated to the container
        - cpu_shares : see docker run docs
        - entrypoint : see docker run docs
        - user : see docker run docs
        - working_dir - see docker run docs
        - command - see docker run docs
        - links - see docker run docs
        - lxc_conf - see docker run docs
        - privileged - see docker run docs
        - dns - see docker run docs
        - volumes_from - see docker run docs
        - network_mode - see docker run docs

    :param profile: The DockerProfile object
    :param overrides: A ContainerOverrides object
    :param kwargs: Keyword args.  See valid keyword args
    :return:
    """

    # 1. check docker images to make sure that the image has been built
    #    if not, then send a subtask to build the image
    # 2. create the container
    # 3. start the container
    # 4. attach to the container
    # 5. remove the container

    if not len(dock.images(name=profile.identifier)) > 0:
        build_image.s(profile)()

    links = {link.name: (link, create_container(link.profile, link.overrides)) for link in profile.links.all()}
    for link, container in links.values():
        if not len(dock.images(name=link.profile.identifier)) > 0:
            build_image.s(link.profile)()

        start_container(container['Id'], link.overrides)

    container = create_container(profile, overrides, **kwargs)
    name = container['Id']

    proc = models.DockerProcess.objects.create(
        profile=profile,
        container_id=name
    )

    here = Site.objects.get_current()
    env = kwargs.get('env', {})
    env['RESPONSE_URL'] = 'http://' + here.domain + reverse('docker-process-finished', {
        'profile_name': profile.name,
        'token': proc.token
    })
    env['ABORT_URL'] = 'http://' + here.domain + reverse('docker-process-aborted', {
        'profile_name': profile.name,
        'token': proc.token
    })
    kwargs['env'] = env
    if len(links):
        kwargs['links'] = {container["Id"]: link_name for link_name, (link, container) in links.items()}

    start_container(profile, name, overrides, **kwargs)

    # bind the task to the runtime of the container. There might be a better way to do this.
    for _ in dock.attach(name, stream=True):
        pass

    output = dock.logs(name)
    proc.logs = output
    dock.remove_container(name)

    return output

@shared_task
def images():
    return dock.images()