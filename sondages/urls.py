from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('sondages.views',
    url(r'^voter/?$','voter'),
    url(r'^scores/?$','scores'),
    url(r'^proposer/?$','proposer'),
    url(r'^valider/?$','valider'),
    url(r'^en-attente/?$','en_attente'),
    url(r'^supprimer/?$','supprimer'),
    url(r'^(?P<indice_sondage>\d+)/json/?$','detail_json'),
)