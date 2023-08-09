from .settings import *

print("This is prod config")
DEBUG=False

ALLOWED_HOSTS = ['45.79.127.173']

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE