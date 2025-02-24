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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DEFAULT_DB_TEST_NAME', 'exportgitlab'),
        'USER': environ.get('DEFAULT_DB_TEST_USER', 'exportgitlab'),
        'PASSWORD': environ.get('DEFAULT_DB_TEST_PASSWORD', 'exportgitlab'),
        'HOST': environ.get('DEFAULT_DB_TEST_HOST', 'localhost'),
        'PORT': environ.get('DEFAULT_DB_TEST_PORT', '5432'),
    }
}

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ['*']

#####################
# Log configuration #
#####################

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
