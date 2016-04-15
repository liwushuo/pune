# -*- coding: utf-8 -*-

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import current_app

from pune.service import UserService
from pune.core import ldap
from pune.utils.auth import login_web
from pune.utils.auth import logout_web
from pune.utils.auth import web_auth_required
from . import bp


@bp.route('/account/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('web/login.html')

    # LDAP login
    uid = request.form.get('uid')
    password = request.form.get('password')

    if not ldap.bind_user(uid, password):
        flash(u'用户名和密码不匹配', 'danger')
        return redirect(url_for('web.login'))

    if not ldap._user_in_auth_groups(uid):
        flash(u'你还没有登录的权限，请联系管理员开通', 'danger')
        return redirect(url_for('web.login'))

    ldap_user = ldap.get_user_details(uid)
    user = UserService.sync_ldap_user(uid, ldap_user['mail'][0],
                                      ldap._user_in_groups(uid, current_app.config['LDAP_ADMIN_GROUP']))
    login_web(user['id'])
    return redirect(url_for('web.dashboard'))


@bp.route('/account/logout')
@web_auth_required
def logout():
    logout_web()
    return redirect(url_for('web.login'))
