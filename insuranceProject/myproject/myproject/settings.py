# myproject/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import cloudinary

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# --- базовое ---
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-very-secret-key-for-local-dev")
DEBUG = os.getenv("DEBUG", "False") == "True"

# Домен(а) продакшена
PROD_HOSTS = ["inschurance.de", "www.inschurance.de", "insurance-1-gt02.onrender.com"]

ALLOWED_HOSTS = ["127.0.0.1", "localhost"] if DEBUG else PROD_HOSTS

# CSRF + прокси
if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_PROXY_SSL_HEADER = None
else:
    # ВАЖНО: сюда обязательно добавь все прод-домены С HTTPS
    CSRF_TRUSTED_ORIGINS = [
        "https://inschurance.de",
        "https://www.inschurance.de",
        "https://insurance-1-gt02.onrender.com",
    ]
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

PREPEND_WWW = False

# Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.sitemaps",
    "insurance",
    "cloudinary",
    "cloudinary_storage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise ДОЛЖЕН идти сразу после SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # у тебя папка называется 'template' — оставляем
        "DIRS": [BASE_DIR / "template"],
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

WSGI_APPLICATION = "myproject.wsgi.application"

# БД
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

LANGUAGE_CODE = "de"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Статика
if DEBUG:
    STATIC_URL = "/static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]
    STATIC_ROOT = BASE_DIR / "staticfiles"
    WHITENOISE_AUTOREFRESH = True
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_DIRS = []  # в проде обычно пусто
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
