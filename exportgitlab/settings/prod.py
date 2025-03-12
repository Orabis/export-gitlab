from .base import *
import os 

##########################
# Database configuration #
##########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD',''),
        'HOST': os.environ.get('DB_HOST','db'),
        'PORT': os.environ.get('DB_PORT','5432'),
    }
}
############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ['192.168.1.174','localhost','0.0.0.0','export.orabis.fr','orabis.fr','www.orabis.fr',]

DEBUG = os.environ.get('DEBUG', '0') == '1'


#####################
# Log configuration #
#####################



##############
# Secret key #
##############

SECRET_KEY = os.environ.get('SECRET_KEY')


############
# Dipstrap #
############

CSRF_TRUSTED_ORIGINS = [
        'https://export.orabis.fr',
        'https://orabis.fr',
        'https://www.orabis.fr',
        'https://api.orabis.fr',
        'http://192.168.1.174:5000',
        'http://localhost:5000',
        'https://localhost:5000',
]

DIPSTRAP_VERSION = os.environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
WKHTML_TO_PDF_URL = "exportgitlab_wkhtmltopdf:9000"

