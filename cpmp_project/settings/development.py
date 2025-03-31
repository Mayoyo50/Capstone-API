from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# In development, allow all hosts
ALLOWED_HOSTS = ['*']

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
]

# Add Debug Toolbar to installed apps
INSTALLED_APPS += [
    'debug_toolbar',
]

# Add Debug Toolbar middleware
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

# Allow your frontend origin
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Default Vite development server port
]

# Email settings (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'