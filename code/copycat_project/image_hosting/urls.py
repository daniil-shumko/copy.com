__author__ = 'Daniil'

from django.conf.urls import patterns, url
from image_hosting import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        # url(r'^?P<category_name>\w+/$', views.index, name='index'),
        # TODO: fix url for different categories
        url(r'^upload/$', views.upload, name='upload'),
        url(r'^image_view/(?P<url_image_name>[\w.]{0,256})$', views.view, name='view'))
