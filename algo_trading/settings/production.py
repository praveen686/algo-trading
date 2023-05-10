import os

from algo_trading.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['algo-trading-dev.ap-south-1.elasticbeanstalk.com', '172.31.11.81']

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True
