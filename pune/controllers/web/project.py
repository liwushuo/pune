# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from pune.service import ProjectService
from pune.service import EnvironmentService
from pune.service import DeployService
from pune.service import UserService
from pune.service import ReleaseService
from pune.models import Deploy
from pune.utils.auth import web_auth_required
from . import bp


@bp.route('/')
@bp.route('/dashboard')
@web_auth_required
def dashboard():
    return render_template('web/dashboard.html')


@bp.route('/projects')
@web_auth_required
def list_projects():

    projects = ProjectService.list_by_status()
    return render_template('web/project/list.html', projects=projects)


@bp.route('/projects/<int:project_id>')
@web_auth_required
def show_project(project_id):
    project = ProjectService.get(project_id)
    envs = EnvironmentService.list_by_project(project_id)
    for env in envs:
        deploys = DeployService.list_by_environment(env['id'], 0, 10)
        env['deploys'] = deploys
        for deploy in deploys:
            deploy['user'] = UserService.get(deploy['operator_id'])
            deploy['release'] = ReleaseService.get(deploy['release_id'])
    return render_template('web/project/show.html', project=project, environments=envs, deploy_status_cn=Deploy.Status._CN)


@bp.route('/projects/add', methods=['GET', 'POST'])
@web_auth_required
def add_project():
    if request.method == 'GET':
        return render_template('web/project/add.html')

    # POST
    name = request.form.get('name')
    scm_url = request.form.get('scm_url')
    cmd = request.form.get('cmd')
    cwd = request.form.get('cwd')
    ProjectService.add(name, scm_url, cmd, cwd)
    flash(u'项目 %s 创建成功' % name, 'success')
    return redirect(url_for('web.list_projects'))


@bp.route('/projects/<int:project_id>/update', methods=['GET', 'POST'])
@web_auth_required
def update_project(project_id):
    project = ProjectService.get(project_id)

    if request.method == 'GET':
        return render_template('web/project/update.html', project=project)

    # POST
    name = request.form.get('name')
    scm_url = request.form.get('scm_url')
    cmd = request.form.get('cmd')
    cwd = request.form.get('cwd')
    ProjectService.update(project_id, name, scm_url, cmd, cwd)
    flash(u'更新成功', 'success')
    return redirect(request.referrer)


@bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@web_auth_required
def delete_project(project_id):
    ProjectService.hide(project_id)
    flash(u'项目删除成功', 'success')
    return redirect(url_for('web.list_projects'))
