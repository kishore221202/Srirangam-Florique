import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ng-flower-shop-2025-payment'

DEBUG = False

ALLOWED_HOSTS = ['*']

# ========================
# INSTALLED APPS
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop',
]

# ========================
# MIDDLEWARE (IMPORTANT FIX)
# ========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ✅ ADD THIS (VERY IMPORTANT)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flowershop.urls'

WSGI_APPLICATION = 'flowershop.wsgi.application'

# ========================
# TEMPLATES
# ========================
TEMPLATES = [{
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
}]

# ========================
# DATABASE
# ========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ========================
# STATIC FILES (FIXED)
# ========================
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# ✅ REQUIRED FOR RENDER
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ========================
# MEDIA FILES (FIXED)
# ========================
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ========================
# DEFAULT FIELD
# ========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================
# SHOP SETTINGS
# ========================
WHATSAPP_NUMBER = '919876543210'
SHOP_UPI_ID     = 'yourname@upi'
SHOP_UPI_NAME   = 'NG Flower Shop'
SHOP_BANK_NAME  = 'State Bank of India'
SHOP_BANK_ACC   = '1234567890'
SHOP_BANK_IFSC  = 'SBIN0001234'
SHOP_BANK_HOLDER= 'NG Srirangam Flower Shop'