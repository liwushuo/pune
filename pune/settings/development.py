# -*- coding: utf-8 -*-

from .base import *


ENV = 'development'
DEBUG = True

SQLALCHEMY_DATABASE_URI = 'mysql://pune:pune@localhost/pune'

ORG_ID_CN = u'上线系统（开发环境）'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['msgpack']
CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_RESULT_SERIALIZER = 'msgpack'

DEPLOY_LOG_PATH = './logs'
RELEASE_UPLOAD_FOLDER = './releases'

# LDAP AUTH
LDAP_LOGIN_ENABLE = True
LDAP_ADMIN_GROUP = ['pune-admin']
LDAP_AUTH_REQUIRE_GROUP = ['pune-user', 'pune-admin']
LDAP_USERS =  {
    'test': (
        'cn=test,ou=people,dc=ldap,dc=liwushuo,dc=com',
        {
            'uid': ['test'],
            'password': ['test'],
            'mail': ['test@liwushuo.com'],
            'uidNumber': ['1000'],
            'displayName': [u'编辑天尊'],
        }
    ),
    'admin': (
        'cn=admin,ou=people,dc=ldap,dc=liwushuo,dc=com',
        {
            'uid': ['admin'],
            'password': ['admin'],
            'mail': ['admin@liwushuo.com'],
            'uidNumber': ['1031'],
            'displayName': [u'江湖骗子'],
        }
    )
}
LDAP_GROUPS = {
    'pune-user': (
        'cn=pune-users,ou=groups,dc=ldap,dc=liwushuo,dc=com',
        {
            'cn': ['pune-users'],
            'memberUid': ['test'],
        }
    ),
    'pune-admin': (
        'cn=pune-admin,ou=groups,dc=ldap,dc=liwushuo,dc=com',
        {
            'cn': ['pune-admin'],
            'memberUid': ['admin'],
        }
    )
}
