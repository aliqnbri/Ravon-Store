from pathlib import Path
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # External Apps
    'debug_toolbar',
    'rest_framework',
    'corsheaders',
    'celery',
   'django_filters',



    # Internal Apps
    'account.apps.AccountConfig',
    'core.apps.CoreConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'cart.apps.CartConfig',
    'customer.apps.CustomerConfig',
    'payment.apps.PaymentConfig',



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'Ecommerce.wsgi.application'


AUTH_USER_MODEL = "account.CustomUser"
CART_SESSION_ID = 'cart'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# BackEnd email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aliqnbri1998@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


# rest framework setting
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':
        'rest_framework.permissions.AllowAny',

    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 5,

    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny',],


    'DEFAULT_AUTHENTICATION_CLASSES': [
        'account.authentications.CustomJWTAuthentication',],


    # 'DEFAULT_SCHEMA_CLASS':
    #     'drf_spectacular.openapi.AutoSchema',
}

AUTHENTICATION_BACKENDS = [
    'account.backend.CustomBackendAuthenticate',
    # 'django.contrib.auth.backends.ModelBackend',  
]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    "TOKEN_OBTAIN_SERIALIZER": "account.serializers.MyTokenObtainPairSerializer",
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    # Cookie name. Enables cookies if value is set.
    'AUTH_COOKIE': 'access_token',
    # A string like "example.com", or None for standard domain cookie.
    'AUTH_COOKIE_DOMAIN': None,
    # Whether the auth cookies should be secure (https:// only).
    'AUTH_COOKIE_SECURE': False,
    # Http only cookie flag.It's not fetch by javascript.
    'AUTH_COOKIE_HTTP_ONLY': True,
    'AUTH_COOKIE_PATH': '/',  # The path of the auth cookie.
    # Whether to set the flag restricting cookie leaks on cross-site requests.
    'AUTH_COOKIE_SAMESITE': 'Lax',
    # This can be 'Lax', 'Strict', or None to disable the flag.
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'Raven Store',
    'DESCRIPTION': 'Django DRF Ecommerce',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

}


# only for Development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = False
CSRF_TRUSTED_ORIGINS = [
    'http://*',
    'https://*',
    'http://127.0.0.1:5500',
    'http://127.0.0.1:8000',
    "http://127.0.0.1",
    "http://localhost",
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'http://127.0.0.1:*', ]
CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:*',
]
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:*',
    # Add other trusted origins as needed
]

# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
# LOGOUT_REDIRECT_URL = 'login'


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

'''ZarinPal Configs'''
MERCHANT = config('MERCHANT')

SANDBOX = True



# Redis settings
REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
REDIS_PORT = config('REDIS_PORT', default='6379')
REDIS_PASS = config('REDIS_PASS')
REDIS_LOCATION = f'redis://{REDIS_HOST}:{REDIS_PORT}' if not REDIS_PASS else \
    f'redis://default:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}'
