# -*- coding: utf-8 -*-

import os

from flask import current_app
from werkzeug import secure_filename

from pune.service import ReleaseService
from pune.utils.text import gen_random_string
from . import bp


@bp.route('/projects/<int:project_id>/releases', methods=['POST'])
def add_release(project_id):
    commit = request.form.get('commit')
    file = request.files['file']

    filename = secure_filename(file.filename)
    file_ext = filename.rsplit('.', 1)[1]

    new_name = '%s.%s' % (gen_random_string(10), file_ext)
    upload_folder = os.path.join(current_app.config['RELEASE_UPLOAD_FOLDER'], str(project_id))
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    file.save(os.path.join(upload_folder, new_name))
    ReleaseService.add(project_id, '%s/%s' % (project_id, new_name), commit)
    return 'OK'
