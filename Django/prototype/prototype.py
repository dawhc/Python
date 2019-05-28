import sys
import os

#defines
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#settings
from django.conf import settings

settings.configure(
    DEBUG = 'on',
    SECRET_KEY = 'ct+zt6v00gm44tq#*oipjlaq6*rj4!4a+*o53ah1jd%a(p&m-h',
    ALLOWED_HOSTS = ['localhost', '127.0.0.1'],
    ROOT_URLCONF = 'sitebuilder.urls',
    MIDDLEWARE_CLASSES = [
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ],
    INSTALLED_APPS = [
        'django.contrib.staticfiles',
        'sitebuilder',
        'compressor',
    ],
    TEMPLATES = [
        {
            'BACKEND' : 'django.template.backends.django.DjangoTemplates',
            'DIRS' : [os.path.join(BASE_DIR, 'sitebuilder/templates')],
            'APP_DIRS' : True,
        }
    ],
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'sitebuilder/static')],
    STATIC_URL = '/static/',
    SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR, 'pages'),
    SITE_OUTPUT_DIRECTORY = os.path.join(BASE_DIR, '_build'),
    STATIC_ROOT = os.path.join(BASE_DIR, '_build', 'static'),
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage',
    STATICFILES_FINDERS= [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder'
    ],
)

#command
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)