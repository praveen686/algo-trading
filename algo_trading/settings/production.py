import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from algo_trading.settings.common import *  # noqa

env = environ.Env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    "malgotrading.com",
    "www.malgotrading.com",
    "172.31.8.67",
    "172.31.33.97",
]

if "RDS_HOSTNAME" in os.environ:  # noqa
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": env("RDS_DB_NAME"),
            "USER": env("RDS_USERNAME"),
            "PASSWORD": env("RDS_PASSWORD"),
            "HOST": env("RDS_HOSTNAME"),
            "PORT": env("RDS_PORT"),
        }
    }

sentry_sdk.init(
    dsn="https://f2df7d9f07244250852c46e2f766ac67@o4505346500067328.ingest.sentry.io/4505346519138304",
    integrations=[
        DjangoIntegration(
            transaction_style="url",
            middleware_spans=True,
            signals_spans=False,
            cache_spans=False,
        ),
    ],
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0.2,
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)
