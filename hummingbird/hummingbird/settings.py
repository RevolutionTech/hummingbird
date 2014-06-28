"""
Django settings for hummingbird project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import config
import hummingbird.settings_environment as senv
import hummingbird.settings_secret as secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

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
    'audiofield',
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
    'audiofield.middleware.threadlocals.ThreadLocals',
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
STATIC_URL = '/static/'
STATICFILES_DIRS = (senv.STATIC_DIR,)
TEMPLATE_DIRS = (senv.TEMPLATE_DIR,)

# Contact
FEEDBACK_EMAIL = senv.FEEDBACK_EMAIL

# Audiofield
MEDIA_ROOT = BASE_DIR + '/' + config.audio_dir
CHANNEL_TYPE_VALUE = 0 # 0-Keep original, 1-Mono, 2-Stereo
FREQ_TYPE_VALUE = 8000 # 0-Keep original, 8000-8000Hz, 16000-16000Hz, 22050-22050Hz, 44100-44100Hz, 48000-48000Hz, 96000-96000Hz
CONVERT_TYPE_VALUE = 0 # 0-Keep original, 1-Convert to MP3, 2-Convert to WAV, 3-Convert to OGG
