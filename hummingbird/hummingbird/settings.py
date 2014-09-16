"""
Django settings for hummingbird project.
"""
import os

import config
import hummingbird.settings_secret as secret

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TOP_DIR = os.path.dirname(BASE_DIR)
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'users',
    'songs',
    'network',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'hummingbird.urls'
WSGI_APPLICATION = 'hummingbird.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'hummingbird',
        'USER': secret.DATABASE_USER,
        'PASSWORD': secret.DATABASE_PASSWORD,
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Templates and static files (CSS, JavaScript, Images)
STATIC_ROOT = STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(TOP_DIR, 'static'),
)
TEMPLATE_DIRS = (
    os.path.join(TOP_DIR, 'templates'),
)

# Contact
FEEDBACK_EMAIL = secret.FEEDBACK_EMAIL

# Song files
MEDIA_ROOT = os.path.join(TOP_DIR, 'audio')
SOUND_DIR = os.path.join(MEDIA_ROOT, 'sound')
