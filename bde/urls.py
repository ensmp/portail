#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

# Les urls concernant les palums sont dans palum/urls.py
urlpatterns = patterns('bde.views',
    url(r'^archives_palum/json/$', 'archives_palum', name='archives_palum_json'),
    url(r'^archives_palum/$', 'archives_palum', name='archives_palum'),
  )
