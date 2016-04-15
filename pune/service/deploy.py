# -*- coding: utf-8 -*-

from datetime import datetime

from flask import current_app

from pune.core import celery
from pune.core import db
from pune.models import Deploy


class DeployService(object):
    @staticmethod
    def get(deploy_id):
        deploy = Deploy.query.get(deploy_id)
        return deploy and deploy.to_dict()

    @staticmethod
    def add(name, project_id, environment_id, release_id, operator_id, task_id):
        deploy = Deploy(name=name, project_id=project_id, environment_id=environment_id,
                        release_id=release_id, operator_id=operator_id, task_id=task_id)
        db.session.add(deploy)
        db.session.commit()
        return deploy.to_dict()

    @staticmethod
    def list_by_environment(environment_id, offset, limit):
        deploys = (Deploy.query.filter_by(environment_id=environment_id)
                               .order_by(Deploy.created_at.desc())
                               .offset(offset)
                               .limit(limit)
                               .all())
        return [deploy.to_dict() for deploy in deploys]

    # TODO: not safe at all...
    @staticmethod
    def count_running_by_environment(environment_id):
        count = Deploy.query.filter_by(environment_id=environment_id, status=Deploy.Status.RUNNING).count()
        return count

    @staticmethod
    def count_by_environment(environment_id):
        count = Deploy.query.filter_by(environment_id=environment_id).count()
        return count

    @staticmethod
    def mark_succeeded(deploy_id):
        Deploy.query.filter_by(id=deploy_id, status=Deploy.Status.RUNNING).update({'status':Deploy.Status.SUCCEEDED, 'finished_at': datetime.utcnow()})
        db.session.commit()

    @staticmethod
    def mark_failed(deploy_id):
        Deploy.query.filter_by(id=deploy_id, status=Deploy.Status.RUNNING).update({'status':Deploy.Status.FAILED, 'finished_at': datetime.utcnow()})
        db.session.commit()

    @staticmethod
    def mark_cancelled(deploy_id):
        Deploy.query.filter_by(id=deploy_id, status=Deploy.Status.RUNNING).update({'status':Deploy.Status.CANCELLED, 'finished_at': datetime.utcnow()})
        db.session.commit()

    @staticmethod
    def cancel_task(deploy_id):
        deploy = Deploy.query.get(deploy_id)
        print deploy.task_id
        celery.control.revoke(deploy.task_id, terminate=False)
        DeployService.mark_cancelled(deploy_id)

    @staticmethod
    def update():
        pass

