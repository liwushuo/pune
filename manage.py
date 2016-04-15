#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['app', 'manager']

import os

from flask_script import Manager
from flask_migrate import MigrateCommand
from werkzeug.contrib.fixers import ProxyFix

from pune.app import create_app
from pune.core import db
from pune.core import celery

flask_env = os.environ.get('FLASK_ENV', 'dev')

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)
manager = Manager(app)

# install commands
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    db.create_all()

@manager.command
def dropdb():
    db.drop_all()

if __name__ == '__main__':
    manager.run()
