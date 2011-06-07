import os.path

BASE_DIR = os.path.dirname(__file__)

def absolute_path(path):
    return os.path.normpath(os.path.join(BASE_DIR, path))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': absolute_path('database.sqlite3'),
    }
}

INSTALLED_APPS = (
    'django.contrib.sites',
    'django_html_filter',
)

ROOT_URLCONF = 'testproject.urls'
TEMPLATE_DIRS = (
    absolute_path('templates'),
)

MIDDLEWARE_CLASSES = (
    'django_html_filter.middleware.HTMLFilterMiddleware',
)
