"""
Django settings for hirebeat project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0j3_3xhym-ma1z7j)t@#0%jg=hjf*nl)9b*98!s4q!ghn^lm%3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    
    # django 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app
    'User',
    'Account',
    
    # frontend style
    'bootstrap5',

    # django-allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', 
    
    # django-invitations
    'invitations',
    
    # Task result storage
     'django_celery_results',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hirebeat.urls'



STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]





TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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
# looking for static files
# STATICFILES_DIRS = [BASE_DIR / "assets"]


WSGI_APPLICATION = 'hirebeat.wsgi.application'

# docker 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
<<<<<<< HEAD
        'NAME': 'hb2023',
        'USER': 'hbuser',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
=======
        'NAME': 'hiredatabase',
        'USER': 'hirebeatdatabase',
        'PASSWORD': '1234567',
        'HOST': 'db',
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
>>>>>>> 420dcff9cd52e32497837e629f183f294b0ff302
    }
}

# local
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'hiredatabase',
#         'USER': 'hirebeatdatabase',
#         'PASSWORD': '1234567',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = '/static/'
# Duplicated?


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'homepage'
LOGIN_URL = 'account_login'
LOGOUT_URL = 'account_logout'
LOGOUT_REDIRECT_URL = 'account_login'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

]


# SMTP service setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yuejiat0416@gmail.com'
EMAIL_HOST_PASSWORD = 'lvevewmkakgfpkkw'


# django-allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {
    'signup': 'User.forms.CustomSignupForm',
}


AUTH_USER_MODEL = 'User.CustomUser'


# Settings for email-invitation
ACCOUNT_ADAPTER = 'invitations.models.InvitationsAdapter'

# INVITATION_MODEL = 'Account.models.TeamInvitation'
# INVITE_FORM = 'Account.forms.InviteForm'
BASE_URL = 'http://localhost:8000'

# Celery configurations

# local
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
# docker 
CELERY_BROKER_URL = 'redis://redis:6379/0'

# this uses django-celery-results to store results in the database
CELERY_RESULT_BACKEND = 'django-db'  
