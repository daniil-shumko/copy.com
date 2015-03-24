__author__ = 'Daniil'

from django.conf.urls import patterns, url
from image_hosting import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^upload/$', views.upload, name='upload'),
        url(r'^image_view/(?P<image_name>[\w.]{0,256})$', views.view_image, name='view'),
        url(r'^professional/$', views.cat_pro, name='pro'),
        url(r'^funny/$', views.cat_funny, name='funny'),
        url(r'^other/$', views.cat_other, name='other'),
        url(r'^most_recent/$', views.cat_recent, name='recent'),
        url(r'^most_up_voted/$', views.cat_up, name='up_voted'),
        url(r'^most_down_voted/$', views.cat_down, name='down_voted'),
        url(r'^random/$', views.random_image, name='random'))
