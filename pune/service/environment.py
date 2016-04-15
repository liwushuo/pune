# -*- coding: utf-8 -*-

from flask import current_app

from pune.core import db
from pune.models import Environment


class EnvironmentService(object):
    @staticmethod
    def get(environment_id):
        env = Environment.query.get(environment_id)
        return env and env.to_dict()

    @staticmethod
    def add(project_id, name, hosts):
        env = Environment(project_id=project_id, name=name, hosts=hosts)
        db.session.add(env)
        db.session.commit()
        return env.to_dict()

    @staticmethod
    def list_by_project(project_id, status=Environment.Status.SHOWN):
        envs = Environment.query.filter_by(project_id=project_id, status=status).all()
        return [env.to_dict() for env in envs]

    @staticmethod
    def hide(environment_id):
        env = Environment.query.get(environment_id)
        env.status = Environment.Status.HIDDEN
        db.session.add(env)
        db.session.commit()

    @staticmethod
    def update(environment_id, name, hosts):
        env = Environment.query.get(environment_id)
        env.name = name
        env.hosts = hosts
        db.session.add(env)
        db.session.commit()
