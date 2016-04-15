# -*- coding: utf-8 -*-

from flask import current_app

from pune.core import db
from pune.models import Release


class ReleaseService(object):
    @staticmethod
    def add(project_id, url, commit):
        release = Release(project_id=project_id, url=url, commit=commit)
        db.session.add(release)
        db.session.commit()

    @staticmethod
    def get(release_id):
        release = Release.query.get(release_id)
        return release and release.to_dict()

    @staticmethod
    def list_by_project(project_id, offset, limit):
        releases = (Release.query.filter_by(project_id=project_id)
                                 .order_by(Release.created_at.desc())
                                 .offset(offset)
                                 .limit(limit)
                                 .all())
        return [release.to_dict() for release in releases]

    @staticmethod
    def count_by_project(project_id):
        count = Release.query.filter_by(project_id=project_id).count()
        return count
