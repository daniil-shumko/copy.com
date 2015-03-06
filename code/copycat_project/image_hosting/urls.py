__author__ = 'Daniil'

from django.conf.urls import patterns, url
from image_hosting import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'))