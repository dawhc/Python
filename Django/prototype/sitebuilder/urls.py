from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.page),
    url(r'^(?P<slug>[\w./-]+)/$', views.page, name = 'page')
]
