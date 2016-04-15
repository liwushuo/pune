# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.dialects.mysql import TINYINT, INTEGER, BIGINT

from pune.core import db
from pune.utils.times import to_timestamp


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('username', name='ux_username'),
        db.UniqueConstraint('email', name='ux_email'),
    )

    class Role(object):
        USER = 0
        ADMIN = 1

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(TINYINT, nullable=False, default=Role.USER)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            username=self.username,
            email=self.email,
            role=self.role,
            created_at=to_timestamp(self.created_at),
            updated_at=to_timestamp(self.updated_at),
        )


class Project(db.Model):
    __tablename__ = 'project'

    class Status(object):
        HIDDEN = 0
        SHOWN = 1

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(TINYINT, nullable=False, default=Status.SHOWN)
    scm_url = db.Column(db.String(200), nullable=True)
    cmd = db.Column(db.String(200), nullable=False)
    cwd = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # provider fixed to fapistrano

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            status=self.status,
            scm_url=self.scm_url,
            cmd=self.cmd,
            cwd=self.cwd,
            created_at=to_timestamp(self.created_at),
            updated_at=to_timestamp(self.updated_at),
        )


class Environment(db.Model):
    __tablename__ = 'environment'

    class Status(object):
        HIDDEN = 0
        SHOWN = 1

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    status = db.Column(TINYINT, nullable=False, default=Status.SHOWN)
    hosts = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            project_id=self.project_id,
            name=self.name,
            status=self.status,
            hosts=self.hosts,
            created_at=to_timestamp(self.created_at),
            updated_at=to_timestamp(self.updated_at),
        )


class Release(db.Model):
    __tablename__ = 'release'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    commit = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            id=self.id,
            project_id=self.project_id,
            url=self.url,
            commit=self.commit,
            created_at=to_timestamp(self.created_at),
        )


class Deploy(db.Model):
    __tablename__ = 'deploy'

    class Status(object):
        RUNNING = 0
        SUCCEEDED = 1
        FAILED = 2
        CANCELLED = 3

        _CN = {
            RUNNING: u'进行中',
            SUCCEEDED: u'成功',
            FAILED: u'失败',
            CANCELLED: u'已取消',
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    environment_id = db.Column(db.Integer, nullable=False)
    release_id = db.Column(db.Integer, nullable=False)
    operator_id = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.String(50), nullable=False)
    status = db.Column(TINYINT, nullable=False, default=Status.RUNNING)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    finished_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            project_id=self.project_id,
            environment_id=self.environment_id,
            release_id=self.release_id,
            operator_id=self.operator_id,
            status=self.status,
            created_at=to_timestamp(self.created_at),
            finished_at=to_timestamp(self.finished_at),
        )
