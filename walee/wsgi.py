"""
WSGI config for walee project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
# gunicorn walee.wsgi:application --bind 0.0.0.0:$PORT

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "walee.settings")

application = get_wsgi_application()
