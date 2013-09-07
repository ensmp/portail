#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

# Les urls concernant les palums sont dans palum/urls.py
urlpatterns = patterns('palum.views',
    url(r'^/archives/json/$', 'archives', name='archives_json'),
    url(r'^archives/$', 'archives', name='archives'),
  )
