from algo_trading.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#tme506+5910b7#6jo1^%o*8xg4=f+@vmxv%2!)#79gi2r8^7y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', 'localhost']

# Generate ERD for models
GRAPH_MODELS = {
    'all_applications': True,
    'graph_models': True,
}
