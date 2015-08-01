"""
WSGI config for labman project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labspy.settings")

application = get_wsgi_application()

from dj_static import Cling
application = Cling(application)