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

Docker Processes is implemented as a Django app and requireds Celery and an AMQP backend that supports broadcast messaging (such as RabbitMQ).  
