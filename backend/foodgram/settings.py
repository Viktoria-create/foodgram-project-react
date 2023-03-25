import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv('SECRET_KEY')
# SECRET_KEY = 'fet80w)=4=u8vwve+yjfxop*p_xmqz%q2p!&m#82r2_o&ptzqa'

DEBUG = int(os.environ.get('DEBUG', default=0))
# DEBUG = True

# ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', '*'), '*']
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '[::1]',
    'testserver',
    ':80',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'djoser',

    'sorl.thumbnail',
    'django_filters',

    'ingredients.apps.IngredientsConfig',
    'recipes.apps.RecipesConfig',
    'tags.apps.TagsConfig',
    'users.apps.UsersConfig',
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

ROOT_URLCONF = 'foodgram.urls'

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

WSGI_APPLICATION = 'foodgram.wsgi.application'

# DATABASES = {
#    'default': {
#        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
#        'NAME': os.getenv('DB_NAME', 'foodgram'),
#       'USER': os.getenv('POSTGRES_USER', 'foodgram_user'),
#        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'foodgram_password'),
#        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
#        'PORT': os.getenv('DB_PORT', '5432')
#    }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
      'NAME':
      'django.contrib.auth.password_validation.'
      'UserAttributeSimilarityValidator',
    },
    {
      'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
      'NAME':
      'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
      'NAME':
      'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'SEARCH_PARAM': 'name'
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
}
