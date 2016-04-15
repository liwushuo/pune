# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from flask import flash
from flask import current_app

from pune.service import UserService
from . import bp


@bp.route('/usrs')
def list_users():
    return 'nothing'
