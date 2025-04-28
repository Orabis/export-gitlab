from .base import *
import os 

BASE_DIR = Path(__file__).resolve().parent.parent.parent

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

ALLOWED_HOSTS = ['unpkg.com','localhost','0.0.0.0','export.orabis.fr','orabis.fr','www.orabis.fr','cdn.orabis.fr']

DEBUG = os.environ.get('DEBUG', '0') == '1'

STATIC_URL = "https://cdn.orabis.fr/"
STATIC_ROOT = '/staticfiles'

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
   	'https://cdn.orabis.fr',
        'https://localhost:5000',
	'https://cdn.orabis.fr/js/vue.esm-browser.prod.js',
	'https://unpkg.com/vue@3.5.13/dist/vue.esm-browser.prod.js',
]
CORS_ALLOWED_ORIGINS = [
        'https://orabis.fr',
        'https://www.orabis.fr',
        'https://api.orabis.fr',
        'http://0.0.0.0',
        'http://192.168.1.174:5000',
        'http://localhost:5000',
        'https://localhost:5000',
        'https://192.168.1.174:5000',
        'https://stock.orabis.fr',
	'https://cdn.orabis.fr',
	'https://export.orabis.fr',
	'https://cdn.orabis.fr',
	'https://unpkg.com',
]
CSRF_TRUSTED_ORIGINS = [
        'https://orabis.fr',
        'https://www.orabis.fr',
        'https://api.orabis.fr',
        'http://192.168.1.174:5000',
        'http://localhost:5000',
        'https://localhost:5000',
        'https://export.orabis.fr',
	'https://cdn.orabis.fr',
	'https://cdn.orabis.fr/js/vue.esm-browser.prod.js',
	'https://unpkg.com/vue@3.5.13/dist/vue.esm-browser.prod.js',
]
CORS_ORIGIN_WHITELIST = ('https://unpkg.com/vue@3.5.13/dist/vue.esm-browser.prod.js','https://cdn.orabis.fr/js/vue.esm-browser.prod.js','https://cdn.orabis.fr','https://export.orabis.fr','http://localhost:5000','https://localhost:5000','192.168.1.174:5000','https://orabis.fr','orabis.fr','https://www.orabis.fr','www.orabis.fr')
CORS_ALLOW_CREDENTIALS = True
DIPSTRAP_VERSION = os.environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
WKHTML_TO_PDF_URL = "http://exportgitlab_wkhtmltopdf:9005"

