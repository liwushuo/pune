# -*- coding: utf-8 -*-

from flask import current_app

from pune.core import db
from pune.models import Project


class ProjectService(object):
    @staticmethod
    def get(project_id):
        project = Project.query.get(project_id)
        return project and project.to_dict()

    @staticmethod
    def add(name, scm_url, cmd, cwd):
        project = Project(name=name, scm_url=scm_url, cmd=cmd, cwd=cwd)
        db.session.add(project)
        db.session.commit()
        return project.to_dict()

    @staticmethod
    def list_by_status(status=Project.Status.SHOWN):
        projects = Project.query.filter_by(status=status).all()
        return [project.to_dict() for project in projects]

    @staticmethod
    def update(project_id, name, scm_url, cmd, cwd):
        project = Project.query.get(project_id)
        project.name = name
        project.scm_url = scm_url
        project.cmd = cmd
        project.cwd = cwd
        db.session.add(project)
        db.session.commit()

    @staticmethod
    def hide(project_id):
        project = Project.query.get(project_id)
        project.status = Project.Status.HIDDEN
        db.session.add(project)
        db.session.commit()

