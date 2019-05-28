import os
import sys

#settings
from django.conf import settings

debug = os.environ.get('DEBUG', 'on') == 'on'
secret_key = os.environ.get('SECRET_KEY', 'w9!yf1hs94**l!jg+2xmncz^#c(4%0zwp@abh4)t-yn+=)&3k=')
allowed_hosts = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')
base_dir = os.path.dirname(__file__)

settings.configure(
	DEBUG = debug,
	SECRET_KEY = secret_key,
	ALLOWED_HOSTS = allowed_hosts,
	ROOT_URLCONF = __name__,
	MIDDLEWARE_CLASSES = [
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware'
	],
    INSTALLED_APPS = [
        'django.contrib.staticfiles'    
    ],
    TEMPLATES = [
        {
            'BACKEND' : 'django.template.backends.django.DjangoTemplates',
            'DIRS' : [os.path.join(base_dir, 'templates')]
        }    
    ],
    STATICFILES_DIRS = [
        os.path.join(base_dir, 'static')
    ],
    STATIC_URL = '/static/'
)


#views
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from imageform import ImageForm
from django.views.decorators.http import etag
import hashlib

def homepage(request):
	return render(request, 'home.html')

def generate_etag(request, width, height):
    content = 'Placeholder: {} x {}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(request, width, height):
    form = ImageForm({'height' : height, 'width' : width})
    if form.is_valid():
        return HttpResponse(form.generate(), content_type = 'image/png')
    else:
        return HttpResponseBadRequest('Invalid Image Request')

def index(request):
    example = reverse('placeholder', kwargs={'width' : 50, 'height' : 50})
    context = {
        'example' : request.build_absolute_uri(example)    
    }
    return render(request, 'index.html', context)


#urls
from django.urls import path
from django.conf.urls import url

urlpatterns = [
    url(r'^index$', index, name = 'index'),
	url(r'^$', homepage, name = 'homepage'),
    url(r'^image/(?P<width>\d+)x(?P<height>\d+)$', placeholder, name = 'placeholder')
]

#wsgi
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

#main
if __name__ == '__main__':
	from django.core.management import execute_from_command_line

	execute_from_command_line(sys.argv)