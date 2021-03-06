"""
WSGI config for case_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


settings_file = f'case_management.{os.getenv("DJANGO_ENV", "settings")}'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_file)
# if os.environ.get('DJANGO_ENV') == 'production':
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_management.production')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'case_management.settings')

application = get_wsgi_application()
