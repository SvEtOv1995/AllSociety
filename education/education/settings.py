import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Настройки для медиафайлов (файлы пользователя, например, изображения)
MEDIA_URL = '/media/'  # URL для доступа к медиафайлам
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Настройки для статических файлов (CSS, JS, изображения)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Путь к папке со статическими файлами
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Папка для собранных статических файлов

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q20=2v-hm^4d7@0nx4!z!=1)yhhy42kjehzodaxhr64d_fdxvr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Настройки для allowed hosts
ALLOWED_HOSTS = [
    '127.0.0.1',  # Локальный хост
    'localhost',   # Локальный хост
    '192.168.68.106',  # IP-адрес вашей машины
    '192.168.68.110',  # Второй IP-адрес вашей машины
]

# Приложения, установленные в проекте
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'courses',  # Добавляем приложение
    'character',
    'schedule',
    'calculator',
]

# Мидлвары, которые обрабатывают запросы и ответы
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной URL конфиг (что будет вызывать корневой файл URL)
ROOT_URLCONF = 'education.urls'

# Шаблоны (templates)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Если вам нужно добавить директорию для шаблонов, добавьте сюда
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

WSGI_APPLICATION = 'education.wsgi.application'


# Настройки базы данных (по умолчанию SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к базе данных
    }
}


# Валидация пароля (по умолчанию включены стандартные валидаторы Django)
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


# Интернационализация (язык и часовой пояс)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Статические файлы (CSS, JavaScript, изображения)
# Параметры настройки статических файлов для разработки и деплоя
STATIC_URL = '/static/'

# Основной ключ для идентификации объектов модели
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
