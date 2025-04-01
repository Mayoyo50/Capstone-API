from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# In development, allow all hosts
ALLOWED_HOSTS = ['localhost',"127.0.0.1"]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

# Add Debug Toolbar to installed apps
INSTALLED_APPS += [
    'debug_toolbar',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Add Debug Toolbar middleware
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'