# -*- coding: utf-8 -*-

from flask import current_app

from werkzeug import generate_password_hash
from werkzeug import check_password_hash

from pune.core import db
from pune.models import User


class UserService(object):

    @staticmethod
    def sync_ldap_user(uid, email, admin=False):
        role = User.Role.ADMIN if admin else User.Role.USER
        user = User.query.filter_by(username=uid).first()

        if user:
            return UserService.update(user.id, role=role)
        else:
            user = User(username=uid, email=email, role=role)
            db.session.add(user)
            db.session.commit()
            return user.to_dict()

    @staticmethod
    def get(user_id):
        user = User.query.get(user_id)
        return user and user.to_dict()

    @staticmethod
    def get_by_email(email):
        user = User.query.filter_by(email=email).first()
        return user and user.to_dict()

    @staticmethod
    def update(user_id, **kw):
        user = User.query.get(user_id)
        fields = set(user.__table__.columns.keys())
        for k, v in kw.items():
            if k not in fields:
                continue
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()
