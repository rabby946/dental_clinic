import os
from pathlib import Path
import environ

# ----------------------
# BASE DIR
# ----------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------
# ENVIRONMENT VARIABLES
# ----------------------
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# ----------------------
# SECRET & DEBUG
# ----------------------
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

# ----------------------
# INSTALLED APPS
# ----------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'apps.core',
    'apps.patients',
    'apps.medicines',
    'apps.prescriptions',
    'apps.billing',
    'apps.notifications',
]

# ----------------------
# MIDDLEWARE
# ----------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dental_clinic.urls'

# ----------------------
# TEMPLATES
# ----------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dental_clinic.wsgi.application'

# ----------------------
# DATABASE (Supabase/PostgreSQL)
# ----------------------
import dj_database_url


DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'), 
        conn_max_age=600
    )
}

# Optional: SSL mode (Supabase requires in production)
DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

# ----------------------
# AUTH PASSWORD VALIDATION
# ----------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ----------------------
# INTERNATIONALIZATION
# ----------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------
# STATIC FILES
# ----------------------
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
