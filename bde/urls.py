from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bde.views',
    url(r'^palums/json/$', 'palums_json', name='palums_json'),
    url(r'^palums/$', 'palums', name='palums'),
    url(r'^voter/$', 'voter', name='voter'),
    url(r'^resultats/$', 'resultats', name='resultats'),
    url(r'^offre_stage/$', 'offre_stage', name='offre_stage'),
    url(r'^voeux_parrainage/$', 'voeux_parrainage', name='voeux_parrainage'),
    url(r'^visualiser_voeux_parrainage/$', 'visualiser_voeux_parrainage', name='visualiser_voeux_parrainage'),
    url(r'^voeux_parrainage_export/$', 'voeux_parrainage_export', name='voeux_parrainage_export'),
    url(r'^voeux_parrainage_algo_export/$', 'voeux_parrainage_algo_export', name='voeux_parrainage_algo_export'),
  )

