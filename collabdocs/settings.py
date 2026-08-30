import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-secret-key")
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h]
CSRF_TRUSTED_ORIGINS = [u for u in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if u]
if render_host := os.environ.get("RENDER_EXTERNAL_HOSTNAME"):
    ALLOWED_HOSTS.append(render_host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_host}")
if vercel_host := os.environ.get("VERCEL_URL"):
    ALLOWED_HOSTS.append(vercel_host)
    CSRF_TRUSTED_ORIGINS.append(f"https://{vercel_host}")
if os.environ.get("VERCEL"):
    ALLOWED_HOSTS.append("draftly-ajaia-assessment.vercel.app")
    CSRF_TRUSTED_ORIGINS.append("https://draftly-ajaia-assessment.vercel.app")

INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "documents",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
ROOT_URLCONF = "collabdocs.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "collabdocs.wsgi.application"
database_url = os.environ.get("DATABASE_URL") or os.environ.get("STORAGE_URL") or os.environ.get("POSTGRES_URL")
if database_url:
    DATABASES = {"default": dj_database_url.parse(database_url, conn_max_age=0 if os.environ.get("VERCEL") else 600)}
    DATABASES["default"].setdefault("OPTIONS", {})
    DATABASES["default"]["OPTIONS"].setdefault("sslmode", "require")
    DATABASES["default"]["OPTIONS"].setdefault("prepare_threshold", None)
else:
    DATABASES = {"default": dj_database_url.parse(f"sqlite:///{BASE_DIR / 'db.sqlite3'}")}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {"staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
