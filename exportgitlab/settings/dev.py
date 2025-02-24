from os import environ
from pathlib import Path

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_NAME='project_name'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db


DATABASES = {
    'default': {
        'ENGINE': environ.get('DEFAULT_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': environ.get('DEFAULT_DB_NAME', 'testdb'),
        'USER': environ.get('DEFAULT_DB_USER', 'dev_dbuser'),
        'PASSWORD': environ.get('DEFAULT_DB_PASSWORD', 'password'),
        'HOST': environ.get('DEFAULT_DB_HOST', 'localhost'),
        'PORT': environ.get('DEFAULT_DB_PORT', '5432'),
    }
}

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ['*']


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
]


############
# Dipstrap #
############

DIPSTRAP_VERSION = environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION


#################
# Debug toolbar #
#################

DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']

WKHTML_TO_PDF_URL = "http://localhost:8001"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
