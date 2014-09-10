# Django Docker Processes 

This project needs a better, more exciting name, because what it allows you to do is actually really exciting.  

## What's it do?

* Allows you to set up image profiles in the Django admin tool, including volumes, ports, and links.
* Lets you set up run profiles for the images, including CPU and memory limits and overridden commands, additional volumes, etcetera. 

With those profiles, docker_processes will:

* Clone any commit of any branch of a git repository, which is assumed to container a Dockerfile (at least)
* Init and update any submodules in that repository
* `docker build` that repository and tag it with a name.
* Run a container from the built images and post the results of running the container back to the requestor.

## Why would I want to do that?

Because you want to set up "canned" processes for people to execute on arbitrary data. Celery tasks are great if you have a well-defined set of tasks to start with, but what if you want to load new tasks at runtime, and what if those tasks come with frankly maniacal sets of dependencies and requirements you don't want to install on your servers running Celery?  

Well, then you use Django Docker Processes to manage those tasks.  This way someone can register a Git repo in Django and their task is encapsulated in that git repo.  They then set up the task so that it executes and pulls all its configuration information from its environment.  Issue a build command for that task and it's ready to go.  

## Requirements

Docker Processes is implemented as a Django app and requireds Celery and an AMQP backend that supports broadcast messaging (such as RabbitMQ). And of course you also need Docker. In short:

* [Celery](http://www.celeryproject.org)
* [RabbitMQ](http://www.rabbitmq.com)
* [Django](http://www.djangoproject.com)
* [Docker](http://www.docker.io)
* django-jsonfield (pip)
* kombu
* Python 2.7
* Git

## Installation

1) Add the `django_docker_processes` app to your `settings.py`'s `INSTALLED_APPS`.  

2) Add something like the below code to settings.py to establish the broadcast and direct queues for dispatching Docker tasks.  Correct the DOCKER_API_VERSION and DOCKER_URL to match your Docker configuration (if you're running Celery in a container, don't forget to make sure that the Docker socket or remote API is available to your celery workers.

    CELERY_DEFAULT_QUEUE = 'default'
    DOCKER_EXCHANGE=Exchange('docker', type='direct')
    DEFAULT_EXCHANGE=Exchange('default', type='topic')
    
    CELERY_QUEUES = (
        Queue('default', routing_key='task.#'),
        Queue('docker_container_tasks', DOCKER_EXCHANGE, routing_key='docker.container'),
        Broadcast('docker_broadcast_tasks', DOCKER_EXCHANGE, routing_key='docker.broadcast'),
    )
    CELERY_DEFAULT_EXCHANGE = 'tasks'
    CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    CELERY_DEFAULT_ROUTING_KEY = 'task.default'
    CELERY_ROUTES = ('django_docker_processes.router.Router',)
    
    DOCKER_URL = 'tcp://192.168.59.103:2375/'
    DOCKER_API_VERSION = '1.12'

3) Run `python manage.py syncdb` to install all the models (or create migrations for South/Django 1.7 if you like)

4) Run celery workers on machines also running Docker daemons listening like this

    $ celery worker -A $(app_name) -E -Q docker_container_tasks,docker_broadcast_tasks

## Caveats

Docker links are not supported yet, as we will need to recursively create and start containers and find a way to bring them back down at the end of the process.  Anyone wants to help with that, the code is in `tasks.py`.  

This code is not terribly well tested, as it was developed over a weekend at the [NCEAS/RENCI Open Science Codefest 2014](http://nceas.github.io/open-science-codefest/) in support of the [Hydroshare](https://github.com/hydroshare) project.  
