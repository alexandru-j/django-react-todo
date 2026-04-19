from os import getenv

from .common import *  # noqa: F401, F403

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = getenv("ALLOWED_HOSTS", "").split()

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DATABASE_NAME"),
        "USER": getenv("DATABASE_USER"),
        "PASSWORD": getenv("DATABASE_PASSWORD"),
        "HOST": getenv("DATABASE_HOST"),
        "PORT": getenv("DATABASE_PORT"),
    }
}
