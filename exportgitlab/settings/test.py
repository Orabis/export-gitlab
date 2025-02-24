import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES['default']['HOST'] = '{{ default_db_host }}'
DATABASES['default']['USER'] = '{{ default_db_user }}'
DATABASES['default']['PASSWORD'] = '{{ default_db_password }}'
DATABASES['default']['NAME'] = '{{ default_db_name }}'


############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "ssl")

#####################
# Log configuration #
#####################

############
# Dipstrap #
############

DIPSTRAP_VERSION = '{{ dipstrap_version }}'
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION
GITLAB_SESSION_COOKIE = '{{ gitlab_session_cookie }}'


SECRET_KEY = '{{ secret_key }}'
