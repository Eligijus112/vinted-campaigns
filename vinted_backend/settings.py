"""
Master settings for the whole of backend
"""

import os
from configurations import Configuration

class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = os.getenv('SECRET_KEY')

    DEBUG = True

    ALLOWED_HOSTS = [
        '0.0.0.0', 
        'localhost', 
        '127.0.0.1', 
        'ec2-13-58-224-148.us-east-2.compute.amazonaws.com',
        '18.191.61.174',
        'ec2-18-191-61-174.us-east-2.compute.amazonaws.com'
        ]

    # Defining installed applications

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'vinted_backend',

        # 3rd party 
        'rest_framework',
        'corsheaders',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    CORS_ORIGIN_WHITELIST = [
        'localhost:3000',
        '127.0.0.1:3000',
        'localhost:2999',
        'ec2-13-58-224-148.us-east-2.compute.amazonaws.com:3000',
        'ec2-13-58-224-148.us-east-2.compute.amazonaws.com:8888',
        'ec2-18-191-61-174.us-east-2.compute.amazonaws.com:8888',
        'localhost:8888'
    ]

    ROOT_URLCONF = 'vinted_backend.urls'

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

    WSGI_APPLICATION = 'vinted_backend.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': os.getenv('DBHOST'),
            'USER': os.getenv('DBUSER'),
            'PASSWORD': os.getenv('DBPASSWORD'),
            'NAME': os.getenv("DBNAME"),
            'PORT': 5432
        }
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

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static")
    ]

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = '/media/'


class Dev(Base):
    def __init__(self):
        super().__init__()
        
        self.DEBUG = True


class Prod(Base):
    def __init__(self):
        super().__init__()
        
        self.DEBUG = False