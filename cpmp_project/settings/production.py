import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': 'capstone-capstone-33.c.aivencloud.com',
        'PORT': 11911,
        'OPTIONS': {
            'sslmode': 'require',
            'sslrootcert': os.path.join(BASE_DIR, 'ca.pem'), 
        },
    }
}


# Production hosts
ALLOWED_HOSTS = [
    os.environ.get('RENDER_HOSTNAME', 'capstone-api-issr.onrender.com'),
]

# Security settings for production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    os.environ.get('FRONTEND_URL'), "https://capstone-rho-nine.vercel.app","https://capstone-7.netlify.app"
]

# Email settings (for production, configure your email service)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')