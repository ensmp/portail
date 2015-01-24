from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from trombi.views import AjouterMaitrise, ModifierMaitrise, SupprimerMaitrise

urlpatterns = patterns('trombi.views',
    url(r'^$', 'trombi'),
    url(r'^json/$', 'trombi_json'),
    url(r'^edit/?$', 'edit'),
    url(r'^instruments/modifier/?$', 'edit_instruments'),
    url(r'^instruments/ajouter/$', login_required(AjouterMaitrise.as_view()), name="ajouter_maitrise"),
    url(r'^instruments/modifier/(?P<pk>\d+)$', login_required(ModifierMaitrise.as_view()), name="modifier_maitrise"),
    url(r'^instruments/supprimer/(?P<pk>\d+)$', login_required(SupprimerMaitrise.as_view()), name="supprimer_maitrise"),
    url(r'^avatar/', include('avatar.urls')), 
    url(r'^octo_update/$', 'octo_update'),
    url(r'^separation/graphe_chemin/$', 'graphe_chemin'),
    url(r'^separation/graphe_mine/$', 'graphe_mine'),
    url(r'^separation/$', 'separation'),
    url(r'^trombi.vcf$', 'get_vcf'), 
    url(r'^(?P<mineur_login>\w+)/?$', 'detail'),
    url(r'^(?P<mineur_login>\w+)/json/$', 'detail_json'),
)