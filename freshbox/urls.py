from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('freshbox.views',
    url(r'^catalogueFresh/$','catalogueFresh'),
    url(r'^commande/$','commande'),
    url(r'^acheter/$','acheter'),
    url(r'^valider_commande/$','valider_commande'),
    url(r'^supprimer_commande/$','supprimer_commande'),
    url(r'^credit_eleve/$','credit_eleve'),
    url(r'^fermer_commandes/$','fermer_commandes'),
    url(r'^dernieres_commandes/$','dernieres_commandes_csv'),
    url(r'^export_soldes/$','export_soldes_csv'),
)