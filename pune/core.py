# -*- coding: utf-8 -*-

__all__ = ['db']

from flask.ext.sqlalchemy import SQLAlchemy
from raven.contrib.flask import Sentry
from flask_migrate import Migrate
from flask.ext.celery import Celery
from flask_ldap import LDAP


db = SQLAlchemy()
sentry = Sentry()
migrate = Migrate()
ldap = LDAP()
celery = Celery()
