#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('jump.views',
    url(r'^etudes/$','etudes'),
)