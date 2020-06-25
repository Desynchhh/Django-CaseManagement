import os
from .settings import *

# Configure default domain name
ALLOWED_HOSTS = [os.environ['WEBSITE_SITE_NAME'] + '.azurewebsites.net', '127.0.0.1'] if 'WEBSITE_SITE_NAME' in os.environ else []

DEBUG = False

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
STATIC_URL = '/static_root/'

# Configure Postgres database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DBNAME'],
        'HOST': os.environ['DBHOST'],
        'USER': os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS']
    }
}