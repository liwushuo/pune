# -*- coding: utf-8 -*-

import os

from flask import render_template
from flask import request
from flask import current_app
from flask import send_from_directory

from pune.service import ReleaseService
from pune.service import ProjectService
from pune.utils.auth import web_auth_required
from pune.utils.pagination import Pagination
from . import bp


@bp.route('/projects/<int:project_id>/releases')
@web_auth_required
def list_releases_by_project(project_id):
    page = request.args.get('page', 1, type=int)
    count = request.args.get('count', 20, type=int)

    project = ProjectService.get(project_id)
    releases = ReleaseService.list_by_project(project_id, (page-1)*count, count)
    releases_count = ReleaseService.count_by_project(project_id)
    pagination = Pagination(page, count, releases_count)
    return render_template('web/release/list.html', project=project, releases=releases, pagination=pagination)


@bp.route('/releases/<int:release_id>/file')
def get_release_file(release_id):
    release = ReleaseService.get(release_id)
    file_path = os.path.join(current_app.config['RELEASE_UPLOAD_FOLDER'], release['url'])
    return send_from_directory(os.path.abspath(os.path.dirname(file_path)), os.path.basename(file_path))
