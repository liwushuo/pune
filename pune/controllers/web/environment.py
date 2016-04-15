# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from pune.service import EnvironmentService
from pune.service import ProjectService
from pune.utils.auth import web_auth_required
from . import bp


@bp.route('/environments/<int:environment_id>')
@web_auth_required
def show_environment(environment_id):
    pass


@bp.route('/projects/<int:project_id>/environments/add', methods=['GET', 'POST'])
@web_auth_required
def add_environment(project_id):
    project = ProjectService.get(project_id)
    if request.method == 'GET':
        return render_template('web/environment/add.html', project=project)

    # POST
    name = request.form.get('name')
    hosts = request.form.get('hosts')
    EnvironmentService.add(project_id, name, hosts)
    flash(u'环境 %s 创建成功' % name, 'success')
    return redirect(url_for('web.show_project', project_id=project_id))


@bp.route('/environments/<int:environment_id>/update', methods=['GET', 'POST'])
@web_auth_required
def update_environment(environment_id):
    env = EnvironmentService.get(environment_id)
    project = ProjectService.get(env['project_id'])
    if request.method == 'GET':
        return render_template('web/environment/update.html', project=project, environment=env)

    # POST
    name = request.form.get('name')
    hosts = request.form.get('hosts')
    EnvironmentService.update(environment_id, name, hosts)
    flash(u'更新成功', 'success')
    return redirect(request.referrer)


@bp.route('/environments/<int:environment_id>/delete', methods=['POST'])
@web_auth_required
def delete_environment(environment_id):
    env = EnvironmentService.get(environment_id)
    project = ProjectService.get(env['project_id'])
    EnvironmentService.hide(environment_id)
    flash(u'环境删除成功', 'success')
    return redirect(url_for('web.show_project', project_id=project['id']))
