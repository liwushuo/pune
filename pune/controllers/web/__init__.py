# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import g

from pune.utils.auth import is_web_login
from pune.utils.auth import get_web_user_id
from pune.service import UserService

bp = Blueprint('web', __name__)

from . import user
from . import project
from . import release
from . import environment
from . import deploy


@bp.before_request
def before_request():
    if is_web_login():
        g.user = UserService.get(get_web_user_id())
