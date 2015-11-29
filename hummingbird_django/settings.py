"""
Django settings for hummingbird_django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ujdo90h)l_xw$^6rj@tnmjg+^0e6zfs1cs$!vnlngjqibpg1$q'

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
    'hummingbird',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hummingbird_django.urls'

WSGI_APPLICATION = 'hummingbird_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


MEDIA_URL = '/'
MEDIA_ROOT = os.path.join(BASE_DIR)

TEMPLATE_PATH = os.path.join(BASE_DIR,'templates')

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
    )

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'



# Main Settings
PLAY_UNKNOWNS = False

# Time Settings
import datetime
TIME_RESET_TIME = datetime.time(hour=4, minute=0) # 4:00am
TIME_WAIT_TO_PLAY = 60 * 5 # 5 minutes
TIME_DELAY_TO_PLAY_SONG = 3
#time_check_queue = 0.25
TIME_CHECK_QUEUE = 1
TIME_INPUT_TIMEOUT = 30
TIME_MAX_SONG_LENGTH = 20
TIME_FADEOUT_SONG = 3000 # in milliseconds

# User Files
DATA_FILE = "songs.csv"
AUDIO_DIR = "audio/"
RANDOM_SUBDIR = "random/"
SOUND_SUBDIR = "sound/"
TCPDUMP_DID_NOT_MATCH_LOG = "tcpdump_dnm.log"

# Data Settings
DO_NOT_PLAY = "DNP"
NEED_TO_ASSIGN = "NTA"
UNKNOWN_USER_PREFIX = "Unknown #"
UNKNOWN_USER_SUFFIX_LENGTH = 5
