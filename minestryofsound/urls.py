#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('minestryofsound.views',
    url(r'^nouveau/$','nouveau'),
    url(r'^playlist/$','playlist'),
    url(r'^playlist/json/$','playlist_json'),
    url(r'^playlist.xml$','playlist_xml'),
    url(r'^player/$','playlist_popup'),
)