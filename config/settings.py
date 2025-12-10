import os
import dj_database_url
from pathlib import Path

REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    # Don't crash if python-dotenv is missing
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "shrouded-sea-15354-891c79e28258.herokuapp.com", "shrouded-sea-15354-cd819052cb94.herokuapp.com"]
CSRF_TRUSTED_ORIGINS = ["https://*.herokuapp.com", ]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition
INSTALLED_APPS = [
    "daphne",
    "home.apps.HomeConfig",
    "user.apps.UserConfig",
    "messaging.apps.MessagingConfig",
    'marketplace.apps.MarketplaceConfig',
    "moderation.apps.ModerationConfig",
    "reports.apps.ReportsConfig",
    "crispy_forms",
    "channels",
    'crispy_bootstrap4',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    "storages",  # for S3 integration

    #google auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

]
 
ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # for static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",#google auth
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "user.middleware.ForceProfileCompletionMiddleware",
    "config.db_middleware.HerokuDatabaseMiddleware",  # Close DB connections for Heroku
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
import dj_database_url
import os

# Default to SQLite (Local Development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# If DATABASE_URL is present (Heroku or local overrides), parse it
if os.environ.get("DATABASE_URL"):
    db_from_env = dj_database_url.config(conn_max_age=600)
    DATABASES["default"].update(db_from_env)

    # ONLY apply SSL and connection pooling if the engine is actually PostgreSQL
    # This prevents crashing if you have a local sqlite DATABASE_URL
    if 'postgresql' in DATABASES["default"]["ENGINE"]:
        DATABASES["default"]["OPTIONS"] = {'sslmode': 'require'}
        DATABASES["default"]["CONN_MAX_AGE"] = 0
        DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
        DATABASES["default"]["ATOMIC_REQUESTS"] = True


# if os.environ.get("DATABASE_URL"):
#     # Heroku or production environment - use more aggressive connection settings
#     database_config = dj_database_url.config(ssl_require=True)
#
#     # Override with production-optimized settings for Heroku
#     database_config.update({
#         'CONN_MAX_AGE': 0,  # No connection pooling for Heroku to prevent connection leaks
#         'CONN_HEALTH_CHECKS': True,  # Enable connection health checks
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#         'ATOMIC_REQUESTS': True,  # Enable atomic transactions
#     })
#
#     DATABASES = {"default": database_config}
# else:
#     # No DATABASE_URL present → fallback to SQLite
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "America/New_York"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Enable WhiteNoise for static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_REDIRECT_URL = 'app-home'

LOGIN_URL = 'login'

#google auth
SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGOUT_REDIRECT_URL = 'app-home'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '169512992077-35db8krbdhgnjkuugofk2uecatd4c61c.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

SOCIALACCOUNT_ADAPTER = 'user.adapter.CustomSocialAccountAdapter'

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')  # Default to us-east-1
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = None
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
# Add connection optimization settings
AWS_S3_MAX_POOL_CONNECTIONS = 50
AWS_S3_RETRIES = {
    'max_attempts': 3,
    'mode': 'adaptive'
}
# Media files configuration
AWS_LOCATION = "media"   # this is REQUIRED for S3
if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'config.storage_backends.MediaStorage'
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

# ============================================================
# EMAIL CONFIGURATION: Local (console) vs Heroku (SMTP)
# ============================================================
ACCOUNT_EMAIL_VALIDATORS = [
    "user.validators.validate_school_email"
]
ACCOUNT_FORMS = {
    "signup": "user.forms.CustomSignupForm",
}
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER') # Your gmail address
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS') # Your App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

# Database connection debugging and logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'WARNING',  # Set to DEBUG to see all SQL queries
        },
        'config.db_middleware': {
            'handlers': ['console'],
            'level': 'INFO',  # Log database middleware actions
        },
    },
}

# Add production-specific database monitoring
if os.environ.get("DATABASE_URL") and not DEBUG:
    # Enable more detailed logging in production to track connection issues
    LOGGING['loggers']['django.db.backends']['level'] = 'ERROR'
    LOGGING['loggers']['config.db_middleware']['level'] = 'WARNING'


