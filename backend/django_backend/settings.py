"""
Django settings for django_backend project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#SMTP

#Email Config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str, default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=str, default='587')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True) # port 587 default
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False) # port 465 default
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str, default=None)
DEFAULT_FROM_EMAIL = config('ADMIN_USER_EMAIL', cast=str, default=None)
ADMIN_USER_NAME = config('ADMIN_USER_NAME', cast=str, default= 'Admin User')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL', cast=str, default= None)


ADMINS=[]

MENEGERS=[]

if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS.append((ADMIN_USER_NAME, ADMIN_USER_EMAIL))
    MENEGERS = ADMINS

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str, default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', '0.0.0.0', '165.22.76.137', 'diplomaroad.pro', 'www.diplomaroad.pro', 'www.diplomaroad.pro:1773', 'api.diplomaroad.pro']

AUTH_USER_MODEL = 'useraccounts.USER'

SITE_ID = 1

# if DEBUG:
#     WEBSITE_URL = 'http://localhost:8010'
# else:
# WEBSITE_URL = 'http://165.22.76.137:1337'
# FRONTEND_URL = "https://www.diplomaroad.pro" 
WEBSITE_URL = 'http://www.diplomaroad.pro:1773'
FRONTEND_URL = 'https://www.diplomaroad.pro'



CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "SIGNING_KEY": 'acomplexkey',
    "ALGORITHM": "HS512",
}
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
# Disable email confirmation
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # This will skip email verification after registration
ACCOUNT_CONFIRM_EMAIL_ON_GET = False  # Disable the email confirmation link trigger
ACCOUNT_EMAIL_REQUIRED = True  # Ensure email is required for registration
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # Ensure users authenticate with their email
#SOCIAL ACCOUNT
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication
    'allauth.account.auth_backends.AuthenticationBackend',  # Allauth backend
]
CORS_ALLOW_ALL_ORIGINS = False  # Restrict to specific origins

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'),
        },
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
        'FETCH_USERINFO': True
    },
    'github': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GITHUB_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GITHUB_OAUTH2_SECRET'),
            'key': ''
        }
    }
}
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_LOGIN_ON_GET = True
USE_X_FORWARDED_HOST = True
GOOGLE_OAUTH2_REDIRECT_URI = 'https://api.diplomaroad.pro/api/auth/google/callback/'
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
LOGIN_REDIRECT_URL = "https://www.diplomaroad.pro/"
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',    
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = [
    'https://diplomaroad.pro', 
    'https://www.diplomaroad.pro',
    'http://127.0.0.1:3000',
    'http://www.diplomaroad.pro:1773',
    'http://165.22.76.137',
    'https://api.diplomaroad.pro',
    'http://165.22.76.137:1337'
]

CSRF_TRUSTED_ORIGINS = [
    'https://diplomaroad.pro', 
    'https://www.diplomaroad.pro', 
    'http://127.0.0.1:3000',
    'https://api.diplomaroad.pro',
    'http://www.diplomaroad.pro:1773',
    'http://165.22.76.137',
    'http://165.22.76.137:1337'
]
CORS_ORIGINS_WHITELIST = [
    'http://127.0.0.1:8010',
    'https://api.diplomaroad.pro',
    'http://127.0.0.1:3000',
    'http://165.22.76.137',
    'http://www.diplomaroad.pro:1773',
    'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 
    'https://www.diplomaroad.pro',
]
CORS_ALLOW_ALL_ORIGINS = True

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False
}
# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #installed app
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'allauth',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.account',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'corsheaders',  # Make sure this line is separate
    'django_celery_beat',
    'django_celery_results',
    #myapps
    'useraccounts',
    'property',
    'chat',
    'inquiries',
    'my_stripe',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # external midlleware
    'allauth.account.middleware.AccountMiddleware',  # Add this line
]


ROOT_URLCONF = 'django_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'django_backend.wsgi.application'
ASGI_APPLICATION = "django_backend.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',  # Ensure this points to a writable directory
#     }
# }



DATABASES = {
    'default': {
        'ENGINE': config("SQL_ENGINE"),
        'NAME': config('SQL_DATABASE'),
        'USER': config('SQL_USER'),
        'PASSWORD': config('SQL_PASSWORD'),
        'HOST': config('SQL_HOST'),
        'PORT': config('SQL_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"
# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', default='redis://localhost:6379')
# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


#STRIPE KEYS
STRIPE_PUBLISH_KEY = config('STRIPE_PUBLISH_KEY', cast=str, default=None)
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', cast=str, default=None)
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', cast=str, default=None)