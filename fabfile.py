# -*- encoding: utf-8 -*-

from fabric.api import task, run, local, prefix, hide, show, abort, with_settings
from fabric.state import env
from fabric.contrib.files import exists
from fapistrano import deploy
from fapistrano.utils import register_env, register_role, green_alert


@task
def runserver(port=5000):
    local('find . -name "*.pyc" -exec rm -rf {} \;', capture=False)
    local("python manage.py runserver -p %s" % port, capture=False)

@task
def celery():
    local('celery -A manage.celery worker -l info', capture=False)

@task
def build_static():
    local('cd pune/frontend && fis release -Lcmpwd ../')
