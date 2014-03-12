#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('minesmarket.views',
    url(r'^catalogue/$','catalogue'),
    url(r'^catalogue_metro/$','catalogue_metro'),
    url(r'^commande/$','commande'),
    url(r'^acheter/$','acheter'),
    url(r'^supprimer_achat/(?P<id_achat>\d+)/$','supprimer_achat'),
    url(r'^supprimer_tous_achats/$','supprimer_tous_achats'),
    url(r'^valider_commande/$','valider_commande'),
    url(r'^credit_eleve/$','credit_eleve'),
    url(r'^fermer_commandes/$','fermer_commandes'),
    url(r'^dernieres_commandes/$','dernieres_commandes_csv'),
    url(r'^export_soldes/$','export_soldes_csv'),
)