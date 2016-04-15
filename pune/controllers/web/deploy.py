# -*- coding: utf-8 -*-

import os

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app
from flask import jsonify
from celery import uuid

from pune.service import ProjectService
from pune.service import EnvironmentService
from pune.service import ReleaseService
from pune.service import DeployService
from pune.service import UserService
from pune.models import Deploy
from pune.utils.auth import web_auth_required
from pune.utils.auth import get_web_user_id
from pune.utils.logtailer import get_history
from pune.utils.pagination import Pagination
from pune.task import run_deploy
from . import bp


@bp.route('/projects/<int:project_id>/releases/<int:release_id>/deploys/add', methods=['GET', 'POST'])
@web_auth_required
def add_deploy(project_id, release_id):
    project = ProjectService.get(project_id)
    release = ReleaseService.get(release_id)
    if request.method == 'GET':
        envs = EnvironmentService.list_by_project(project_id)
        return render_template('web/deploy/add.html', project=project, release=release, environments=envs)

    # POST
    user_id = get_web_user_id()
    environment_id = request.form.get('environment_id', type=int)
    name = request.form.get('name')
    task_id = uuid()

    count = DeployService.count_running_by_environment(environment_id)
    if count >= 1:
        flash(u'当前环境下有正在部署的任务，请先等待执行完', 'danger')
        return redirect(request.referrer)

    env = EnvironmentService.get(environment_id)
    deploy = DeployService.add(name, project_id, environment_id, release_id, user_id, task_id)

    cmd = project['cmd']
    cmd = cmd.replace('{environment}', env['name'])
    cmd = cmd.replace('{url}', release['url'])
    run_deploy.apply_async((cmd, project['cwd'], deploy['id']), task_id=task_id)
    return redirect(url_for('web.show_deploy', deploy_id=deploy['id']))


@bp.route('/deploys/<int:deploy_id>')
@web_auth_required
def show_deploy(deploy_id):
    deploy = DeployService.get(deploy_id)
    project = ProjectService.get(deploy['project_id'])
    env = EnvironmentService.get(deploy['environment_id'])
    return render_template('web/deploy/show.html', deploy=deploy, project=project, environment=env)


@bp.route('/deploys/<int:deploy_id>/cancel')
@web_auth_required
def cancel_deploy(deploy_id):
    DeployService.cancel_task(deploy_id)
    return redirect(request.referrer)


@bp.route('/deploys/<int:deploy_id>/log')
@web_auth_required
def tailf_deploy_log(deploy_id):
    last_position = request.args.get('last_position', type=int)

    # f = open('/Users/maple/Documents/Code/personal/scale/all.log', 'r')
    f = open('%s/%s.log' % (current_app.config['DEPLOY_LOG_PATH'], deploy_id), 'r')

    content = []
    if not last_position:
        content = get_history(f)
    else:
        f.seek(0, os.SEEK_END)
        if last_position <= f.tell():
            f.seek(last_position)
        for line in f:
            content.append(line)

    last_position = f.tell()
    f.close()
    return jsonify(content=content, last_position=last_position)


@bp.route('/environments/<int:environment_id>/deploys')
def list_deploys_by_environment(environment_id):
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 20, type=int)
    env = EnvironmentService.get(environment_id)

    project = ProjectService.get(env['project_id'])
    deploys = DeployService.list_by_environment(environment_id, (page-1)*count, count)
    for deploy in deploys:
        deploy['user'] = UserService.get(deploy['operator_id'])
        deploy['release'] = ReleaseService.get(deploy['release_id'])
    deploys_count = DeployService.count_by_environment(environment_id)
    pagination = Pagination(page, count, deploys_count)
    return render_template('web/deploy/list.html', deploys=deploys, project=project, environment=env, pagination=pagination, deploy_status_cn=Deploy.Status._CN)
