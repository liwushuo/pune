# -*- coding: utf-8 -*-

__all__ = ['create_app']

from os import environ

from flask import Flask

from pune.core import db
from pune.core import sentry
from pune.core import migrate


def config_from_env(config=None):
    config_map = {
        'dev': 'pune.settings.development',
        'prod': 'pune.settings.production',
    }

    flask_env = environ.get('FLASK_ENV', 'dev')
    return config_map.get(flask_env, config_map['dev'])


def create_app(config=None):
    if not config:
        config = config_from_env()

    app = Flask(__name__)

    configure_app(app, config)
    configure_extensions(app)
    configure_filters(app)
    configure_blueprints(app)
    return app


def configure_app(app, config):
    app.config.from_object(config)


def configure_extensions(app):
    db.init_app(app)

    migrate.init_app(app, db)

    sentry.init_app(app)


def configure_blueprints(app):
    from pune.controllers import web_bp, admin_bp, api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(admin_bp, url_prefix='/expune')
    app.register_blueprint(api_bp, url_prefix='/api')


def configure_filters(app):
    pass
