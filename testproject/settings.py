# test project django settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'name': ':memory:',
    },
}

ROOT_URLCONF = 'testproject.urls'
SECRET_KEY = 's3cr3t'

INSTALLED_APPS = (
    'formulation',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'testproject', 'templates'),
)

try:
    from django.test.runner import DiscoverRunner
except:
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
