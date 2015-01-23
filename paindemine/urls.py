#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('paindemine.views',
    url(r'^catalogue_pain/$', 'catalogue_pain', name='catalogue_pain'),
    url(r'^commande/$', 'commande', name='commande'),
    url(r'^acheter/$', 'acheter', name='acheter'),
    url(r'^supprimer_achat/(?P<id_achat>\d+)/$', 'supprimer_achat', name='supprimer_achat'),
    url(r'^supprimer_tous_achats/$', 'supprimer_tous_achats', name='supprimer_tous_achats'),
    url(r'^fermer_commandes/$', 'fermer_commandes', name='fermer_commandes'),
	url(r'^dernieres_commandes/$', 'dernieres_commandes_csv', name='dernieres_commandes'),
    url(r'^soldespaindemine/$','soldespaindemine'),
    url(r'^affichagesoldes/$','affichagesoldes')
)

