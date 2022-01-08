"""
Django settings for backups project.
"""

import os

from rich.console import Console

from backups.config import BackupsConfig

console = Console()
cnf = BackupsConfig()

ADMINS = [('Dimitris', 'dstrants@gmail.com')]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = cnf.django_secret
ALLOWED_HOSTS = cnf.allowed_hosts or ['localhost']

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'sync.integrations.todoist.strategy.TodoistOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'social_django',
    'rest_framework',
    'rest_framework.authtoken',
    'django_dramatiq',
    'django_periodiq',
    'anymail',
    'dbbackup',
    'logs',
    'productivity',
    'profiles',
    'sync'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]
ROOT_URLCONF = 'backups.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['./templates'],
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
WSGI_APPLICATION = 'backups.wsgi.application'
DEBUG = cnf.debug

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level':  cnf.log_level,
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': cnf.db_name,
        'USER': cnf.db_user,
        'HOST': cnf.db_host,
        'PORT': cnf.db_port
        }
}
if pwd := cnf.db_pass:
    DATABASES['default']['PASSWORD'] = pwd

if cnf.redis_host:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": cnf.redis_host,
            "TIMEOUT": None,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            "KEY_PREFIX": "backups"
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

if cnf.dev:
    STATIC_URL = 'http://localhost:8080/'
else:
    import sentry_sdk
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
    dsn=cnf.sentry_dsn,
    integrations=[DjangoIntegration(), RedisIntegration()])
    USE_X_FORWARDED_HOST = True

    # Https conf
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # Static Files Configuration for Production
    STATIC_URL = '/static/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # Scaleway bucket configuration
    AWS_S3_REGION_NAME = cnf.scaleway_region
    AWS_S3_ENDPOINT_URL = cnf.scaleway_endpoint
    AWS_STORAGE_BUCKET_NAME = cnf.scaleway_bucket

    # Scaleway Credentials
    AWS_ACCESS_KEY_ID = cnf.scaleway_key_id
    AWS_SECRET_ACCESS_KEY = cnf.scaleway_access_key

if cnf.docker:
    console.print('You are using docker env', style='bold bright_cyan')
else:
    console.print('Loading custom config', style='bold magenta')

console.print(f"Using database {DATABASES['default']['NAME']}", style='bold magenta')

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Athens'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = ['dist']

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

LOGIN_URL = 'login'
AFTER_LOGIN_REDIRECT = 'home'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = cnf.google_app_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = cnf.google_app_secret
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]
SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
    'access_type': 'offline',
    'approval_prompt': 'auto'
}
SOCIAL_AUTH_TODOIST_KEY = cnf.todoist_app_key
SOCIAL_AUTH_TODOIST_SECRET = cnf.todoist_app_secret
SOCIAL_AUTH_TODOIST_SCOPE = ['data:read']
SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ALLOWED_HOSTS
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_GITHUB_KEY = cnf.github_app_key
SOCIAL_AUTH_GITHUB_SECRET = cnf.github_app_secret
SOCIAL_AUTH_GITHUB_SCOPE = ['repo']
STATICFILES_DIRS = ['dist']
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "url": cnf.redis_host,
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ]
}

# Defines which database should be used to persist Task objects when the
# AdminMiddleware is enabled.  The default value is "default".
DRAMATIQ_TASKS_DATABASE = "default"
UPTIME_MONITOR_KEY = cnf.up_time_key
MAILGUN_KEY = cnf.mailgun_key

MEDIA_ROOT = 'media/'
MEDIA_URL = 'upload/'

# Email Settings
ANYMAIL = {
    "MAILGUN_API_KEY": cnf.mailgun_key,
    "MAILGUN_SENDER_DOMAIN": 'notify.strdi.me',
    "MAILGUN_API_URL": "https://api.eu.mailgun.net/v3"
}
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@notify.strdi.me'
SERVER_EMAIL = 'backups@notify.strdi.me'

# Database & Media Backups Configuration
DBBACKUP_CLEANUP_KEEP = 10
DBBACKUP_CLEANUP_KEEP_MEDIA = 10
DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': cnf.dropbox_backups_token,
    'root_path': f'backups/{cnf.db_backups_host}',
}
DBBACKUP_HOSTNAME = cnf.db_backups_host
FIXTURE_DIRS = ["./fixtures"]
SLACK_API_TOKEN = cnf.slack_token

MONGO_CONNECTION_STRING=cnf.mongo_db