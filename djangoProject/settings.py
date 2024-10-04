import os
from datetime import timedelta
from pathlib import Path
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = "djangoProject"
PROJECT_DIR = "%s/%s" % (BASE_DIR, PROJECT_NAME)


DEBUG = False if os.getenv("DJANGO_PROD") == "True" else True

print(f"Debug is {DEBUG}")

load_dotenv(dotenv_path=Path(f"./env.{'dev' if DEBUG else 'prod'}-sample"))


SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt.token_blacklist",
    "apps.apirouter.apps.ApirouterConfig",
    "apps.user.apps.UserConfig",
    "apps.page_router.apps.PagerouterConfig",
    "apps.builtin_model.apps.ModelConfig",
    "apps.user.user_models.apps.UserModelsConfig",
    "django_extensions",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "bootstrap5",
    "compressor",
]

if DEBUG:
    INSTALLED_APPS.insert(5, "debug_toolbar")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

# auth

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
# compressor settings(tailwind)
COMPRESS_ROOT = BASE_DIR / "static"

COMPRESS_ENABLED = True

ROOT_URLCONF = "djangoProject.urls"

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




CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS").split(",")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ORIGIN_REGEXES = True
CORS_ALLOW_METHODS = ("GET", "POST", "PUT", "DELETE")
CORS_PREFLIGHT_MAX_AGE = 60 * 60 * 2  # 2 hours

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 2

# not the best practice
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000", "https://127.0.0.1:3000"]

WSGI_APPLICATION = "djangoProject.wsgi.application"
# Database


DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_DATABASE_ENGINE"),
        "NAME": os.getenv("SQL_DATABASE"),
        "USER": os.getenv("SQL_USER"),
        "PASSWORD": os.getenv("SQL_PASSWORD"),
        "HOST": os.getenv("SQL_HOST"),
        "PORT": os.getenv("SQL_PORT"),
    },
}

# rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# simple jwt

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=20),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_DOMAIN': None,
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'LAX',
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
]



if DEBUG:
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ]

INTERNAL_IPS = [
    "127.0.0.1",
]


def show_toolbar(rew):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}
# Internationalization

TIME_ZONE = "UTC"
USE_L10N = True
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",
]
USE_I18N = True
USE_TZ = True
LANGUAGES = [("en", _("English")), ("de", _("German")), ("pl", _("Polish"))]
LANGUAGE_CODE = "en"
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "/var/www/neoai/static/"
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# AWS S3 CONFIG
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_SIGNATURE_NAME = os.getenv("AWS_S3_SIGNATURE_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_FILE_OVERWRITE = os.getenv("AWS_S3_FILE_OVERWRITE")
AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL")
AWS_S3_VERITY = os.getenv("AWS_S3_VERITY")
AWS_S3_BASE_URL = os.getenv("AWS_S3_BASE_URL")

# storages
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {},
    },
}

# HTTPS
# SECURE_HSTS_SECONDS = 30  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# caching
if not DEBUG:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
            "KEY_PREFIX": "example",
        }
    }

LOGIN_REDIRECT_URL = "dashboard/"
LOGOUT_REDIRECT_URL = "/"
