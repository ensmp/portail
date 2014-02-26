from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('trombi.views',
    url(r'^$', 'trombi'),
    url(r'^json/$', 'trombi_json'),
    url(r'^edit/?$', 'edit'),
    url(r'^avatar/', include('avatar.urls')), 
    url(r'^(?P<mineur_login>\w+)/?$', 'detail'),
    url(r'^(?P<mineur_login>\w+)/json/$', 'detail_json'),
    url(r'^octo_update/$', 'octo_update'),
    url(r'^separation/graphe_chemin/$', 'graphe_chemin'),
    url(r'^separation/graphe_mine/$', 'graphe_mine'),
    url(r'^separation/$', 'separation'),
    url(r'^trombi.vcf$', 'get_vcf'), 
)