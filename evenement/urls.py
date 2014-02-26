#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

# Les urls concernant les événements depuis la page d'une association sont dans association/urls.py
urlpatterns = patterns('evenement.views',
    url(r'^$', 'index', name='calendrier'),
    url(r'^json/$', 'index_json', name='calendrier_json'),
    url(r'^(?P<evenement_id>\d+)/supprimer/$', 'supprimer'),
    url(r'^nouveau_calendrier/$', 'nouveau_calendrier', name='nouveau_calendrier'),
    url(r'^supprimer_calendrier/$', 'supprimer_calendrier', name='supprimer_calendrier'),
    url(r'^update_calendrier/$', 'update_calendrier', name='update_calendrier'),
)