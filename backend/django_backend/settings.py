from pathlib import Path
from decouple import config
from datetime import timedelta

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# EMAIL CONFIGURATION
# ==========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', cast=str, default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', cast=str, default='587')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool, default=False)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str, default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str, default=None)
DEFAULT_FROM_EMAIL = config('ADMIN_USER_EMAIL', cast=str, default=None)
ADMIN_USER_NAME = config('ADMIN_USER_NAME', cast=str, default='Admin User')
ADMIN_USER_EMAIL = config('ADMIN_USER_EMAIL', cast=str, default=None)

ADMINS = []
MANAGERS = []
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS.append((ADMIN_USER_NAME, ADMIN_USER_EMAIL))
    MANAGERS = ADMINS

# ==========================
# SECURITY
# ==========================
SECRET_KEY = config('SECRET_KEY', cast=str, default=None)
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = [
    'localhost', '127.0.0.1', '[::1]', '0.0.0.0', '165.22.76.137',
    'diplomaroad.pro', 'www.diplomaroad.pro', 'www.diplomaroad.pro:1773',
    'api.diplomaroad.pro'
]

# ==========================
# AUTHENTICATION AND JWT
# ==========================
AUTH_USER_MODEL = 'useraccounts.USER'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "SIGNING_KEY": 'acomplexkey',
    "ALGORITHM": "HS512",
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'),
            'FETCH_USERINFO': True,
            'OAUTH_PKCE_ENABLED': True,
        },
        'SCOPE': ['email', 'profile'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
    'github': {
        'APP': {
            'client_id': config('SOCIAL_AUTH_GITHUB_OAUTH2_KEY'),
            'secret': config('SOCIAL_AUTH_GITHUB_OAUTH2_SECRET'),
            'key': ''
        },
        'SCOPE': ['user', 'repo'],  # Define necessary permissions
        'AUTH_PARAMS': {
            'force_verify': 'true',
        },
        'METHOD': 'oauth2',
        'API_URL': 'https://api.github.com/user',
    }
}

USE_X_FORWARDED_HOST = True
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_LOGIN_ON_GET = True
GOOGLE_OAUTH2_REDIRECT_URI = 'https://api.diplomaroad.pro/accounts/google/login/callback/'
GITHUB_REDIRECT_URI = 'https://api.diplomaroad.pro/accounts/github/login/callback/'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
LOGIN_REDIRECT_URL = '/callback/'

# ==========================
# CORS and CSRF
# ==========================
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8010', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
    'http://127.0.0.1:3000', 'http://www.diplomaroad.pro:1773',
    'http://165.22.76.137', 'https://api.diplomaroad.pro'
]
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8010', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
    'http://127.0.0.1:3000', 'https://api.diplomaroad.pro',
    'http://www.diplomaroad.pro:1773', 'http://165.22.76.137'
]
CORS_ORIGINS_WHITELIST = [
    'http://127.0.0.1:8010', 'https://api.diplomaroad.pro',
    'http://127.0.0.1:3000', 'http://165.22.76.137',
    'http://www.diplomaroad.pro:1773', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
]

CORS_ALLOW_CREDENTIALS=True

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

WSGI_APPLICATION = 'django_backend.wsgi.application'
ASGI_APPLICATION = "django_backend.asgi.application"
ROOT_URLCONF = 'django_backend.urls'
# ==========================
# DATABASE
# ==========================
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

# ==========================
# INSTALLED APPS
# ==========================
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Installed apps
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
    'corsheaders',  
    'django_celery_beat',
    'django_celery_results',
    # My apps
    'useraccounts',
    'property',
    'chat',
    'inquiries',
    'my_stripe',
]

# ==========================
# MIDDLEWARE
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # External middleware
    'allauth.account.middleware.AccountMiddleware',
]

# ==========================
# CELERY
# ==========================
CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', default='redis://localhost:6379')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# ==========================
# STRIPE CONFIGURATION
# ==========================
STRIPE_PUBLISH_KEY = config('STRIPE_PUBLISH_KEY', cast=str, default=None)
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', cast=str, default=None)
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', cast=str, default=None)

# ==========================
# STATIC AND MEDIA FILES
# ==========================
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ==========================
# DJANGO REST
# ==========================

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'backend.useraccounts.CustomPasswordResetSerializer',
}

REST_AUTH = {
    'USE_JWT': True,
    'JWT_AUTH_HTTPONLY': False,
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # 'REFRESH_TOKEN_LIFETIME': timedelta(days=3)
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        'rest_framework_simplejwt.authentication.JWTAuthentication',    
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# =======================
#        DOMAINS
# =======================

WEBSITE_URL_PROFILE = 'http://www.diplomaroad.pro:1773'
WEBSITE_URL = 'https://api.diplomaroad.pro'
FRONTEND_URL = 'https://www.diplomaroad.pro'
DEFAULT_DOMAIN = 'www.diplomaroad.pro'

SITE_ID = 1


# =======================
# DJANGO TEMPLATES
# =======================

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True