from pathlib import Path
from decouple import config
from datetime import timedelta, datetime
import watchtower
import logging
import sentry_sdk


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
AUTH_USER_MODEL = 'useraccounts.User'
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_EMAIL_VERIFICATION = False
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_ADAPTER = 'useraccounts.adapter.CustomSocialAccountAdapter'

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
CORS_ALLOW_ALL_ORIGINS = True  # Or specify your allowed domains
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8010', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
    'http://127.0.0.1:3000', 'http://www.diplomaroad.pro:1773',
    'http://165.22.76.137', 'https://api.diplomaroad.pro',
]
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8010', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
    'http://127.0.0.1:3000', 'https://api.diplomaroad.pro',
    'http://www.diplomaroad.pro:1773', 'http://165.22.76.137',
]
CORS_ORIGINS_WHITELIST = [
    'http://127.0.0.1:8010', 'https://api.diplomaroad.pro',
    'http://127.0.0.1:3000', 'http://165.22.76.137',
    'http://www.diplomaroad.pro:1773', 'http://165.22.76.137:1337',
    'https://diplomaroad.pro', 'https://www.diplomaroad.pro',
]
CSRF_COOKIE_SECURE=True
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
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10 MB
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
    'drf_yasg',
    # My apps
    'useraccounts',
    'property',
    'chat',
    'inquiries',
    'my_stripe',
    'reviews',
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
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', cast=str, default='django-db')
CELERY_BROKER_URL = config('CELERY_BROKER_REDIS_URL', cast=str, default='redis://localhost:6379')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
CELERY_BEAT_SCHEDULER_MAX_INTERVAL = 60

broker_transport_options = {
    'retry_on_timeout': True,
    'max_retries': 5,
    'interval_start': 0,   # Start retry delay immediately
    'interval_step': 0.2,  # Step-up delay between retries
    'interval_max': 0.5,   # Maximum delay between retries
}
CELERY_WORKER_CONCURRENCY = 4  # Limit the number of concurrent worker threads (adjust as needed)

# Soft and hard task time limits
CELERY_TASK_SOFT_TIME_LIMIT = 300  # Abort task gracefully after 5 minutes
CELERY_TASK_TIME_LIMIT = 360  # Hard limit of 6 minutes

# Prefetch multiplier to control the number of tasks a worker prefetches
CELERY_WORKER_PREFETCH_MULTIPLIER = 1  # Prevent worker from prefetching too many tasks

# Max retries for tasks
CELERY_TASK_MAX_RETRIES = 3

# Task ignore result to avoid storing unnecessary results
CELERY_TASK_IGNORE_RESULT = True  # Set to True if results are not needed
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
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
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
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/hour',
        'login': '10/minute',
    },
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://redis:6379/0")],
        },
    },
}

# =======================
#        DOMAINS
# =======================

WEBSITE_URL_PROFILE = 'https://api.diplomaroad.pro'
WEBSITE_URL = 'https://api.diplomaroad.pro'
FRONTEND_URL = 'https://www.diplomaroad.pro'
DEFAULT_DOMAIN = 'https://www.diplomaroad.pro'

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

#=========================
# AWS LOGS
#=========================
import boto3

logger = logging.getLogger('default')  # Use 'default' logger explicitly

logger_boto3_client = boto3.client(
    'logs',
    aws_access_key_id=config('AWS_ACCESS_KEY', cast=str, default=None),
    aws_secret_access_key=config('AWS_SECRET_KEY', cast=str, default=None),
    region_name='us-east-1'
)
CLOUDWATCH_DEFAULT_LOG_STREAM_NAME = f"app-log-stream-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Log everything to file
            'class': 'logging.FileHandler',
            'filename': '/usr/src/backend/logs/diplomaroad.log',
            'formatter': 'default',
        },
        'cloudwatch': {
            'level': 'INFO',  # Send only INFO and above to CloudWatch
            'class': 'watchtower.CloudWatchLogHandler',
            'boto3_client': logger_boto3_client,
            'log_group': '/diplomaroad-log-group',
            'stream_name': 'manual-test-log-stream',
            'formatter': 'default',
            'send_interval': 60,  # Ensures logs are sent immediately
        },
        'console': {
            'level': 'INFO',  # Show only warnings and above in the console
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        'default': {
            'handlers': ['file', 'cloudwatch', 'console'],  # Log to all handlers
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'cloudwatch', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'botocore': {
            'handlers': ['file'],  # Only log to file to avoid spamming other outputs
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

#=========================
# SENTRY SETUP
#=========================

sentry_sdk.init(
    dsn="https://a2be57323f6ceab15e7015656130e5f3@o4508488518270976.ingest.de.sentry.io/4508488525676624",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

#===========================
# CACHE SETTINGS
#===========================

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/2',  # Use a different DB index if needed
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,  # Avoid crashing if Redis is unavailable
        }
    }
}

#=====================================================
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True