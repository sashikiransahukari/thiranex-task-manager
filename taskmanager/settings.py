from pathlib import Path
import os
import dj_database_url


# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-key"
)

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"


# =========================
# ALLOWED HOSTS
# =========================

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",

    "tasks",
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =========================
# URL CONFIGURATION
# =========================

ROOT_URLCONF = "taskmanager.urls"


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =========================
# WSGI
# =========================

WSGI_APPLICATION = "taskmanager.wsgi.application"


# =========================
# DATABASE
# =========================

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }

else:

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# =========================
# INTERNATIONALIZATION
# =========================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# =========================
# STATIC FILES
# =========================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# =========================
# DEFAULT PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =========================
# LOGIN / LOGOUT
# =========================

LOGIN_URL = "/"

LOGIN_REDIRECT_URL = "/dashboard/"

LOGOUT_REDIRECT_URL = "/"


# =========================
# RENDER HTTPS
# =========================

if not DEBUG:

    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True