import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from decouple import config, UndefinedValueError
import cloudinary
import cloudinary.uploader
import cloudinary.api
import cloudinary_storage

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

DEBUG = os.getenv("DEBUG", "False") == "True"

# --- БЕЗОПАСНОСТЬ: делаем завязку на DEBUG ---
if DEBUG:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
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
    ALLOWED_HOSTS = [
        "inschurance.de",
        "www.inschurance.de",
        "insurance-1-gt02.onrender.com.",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://inschurance.de",
        "https://www.inschurance.de",
    ]
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # Если за прокси (Render/NGINX) — пробрасываем схему
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

PREPEND_WWW = False

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv("DEBUG", "False") == "True"

SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-very-secret-key-for-local-dev')

ALLOWED_HOSTS = ["*"] if DEBUG else ["www.inschurance.de", "inschurance.de", "insurance-1-gt02.onrender.com"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'insurance',
    'cloudinary',
    'cloudinary_storage',
    'django.contrib.sitemaps',
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=not DEBUG  # True на проде, False локально
    )
}

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

LANGUAGE_CODE = 'de'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

if DEBUG:
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [ BASE_DIR / 'static' ]  # где лежат твои css/js при разработке
    STATIC_ROOT = BASE_DIR / 'staticfiles'      # не используется в dev, но пусть будет
    WHITENOISE_AUTOREFRESH = True
else:
    STATIC_URL = '/static/'                     # или твой CDN-путь, если реально нужен
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    STATICFILES_DIRS = []                       # на проде обычно пусто
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

WHITENOISE_AUTOREFRESH = True