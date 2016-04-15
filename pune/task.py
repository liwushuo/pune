# -*- coding: utf-8 -*-

from subprocess import Popen
import shlex
import os

from flask import current_app
from celery.signals import task_revoked

from pune.service import DeployService
from pune.core import celery

@celery.task()
def run_deploy(cmd, cwd, deploy_id):
    try:
        logfile = open('%s/%s.log' % (current_app.config['DEPLOY_LOG_PATH'], deploy_id), 'w+')
        p = Popen(shlex.split(cmd), cwd=cwd, stdout=logfile, stderr=logfile, bufsize=1)
        streamdata = p.communicate()[0]
        logfile.close()
    except:
        DeployService.mark_failed(deploy_id)

    if p.returncode == 0:
        DeployService.mark_succeeded(deploy_id)
    else:
        DeployService.mark_failed(deploy_id)
