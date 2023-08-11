from .settings import *

initial_globals = set(globals().keys())

print("This is prod config")
DEBUG = False

ALLOWED_HOSTS = ["45.79.127.173"]

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MIDDLEWARE = ["whitenoise.middleware.WhiteNoiseMiddleware"] + MIDDLEWARE


# Store the changed global variables
changed_globals = set(globals().keys())

# Store the changed global variables


# Find the difference between initial and changed variables
changed_variables = changed_globals - initial_globals

# Print the changed variables
print("Changed variables:", changed_variables)
