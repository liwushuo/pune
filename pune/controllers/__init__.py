# -*- coding: utf-8 -*-

__all__ = ['web_bp', 'admin_bp', 'api_bp']

from .web import bp as web_bp
from .admin import bp as admin_bp
from .api import bp as api_bp
