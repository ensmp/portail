from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bde.views',
    url(r'^campagne/voter/$', 'voter', name='campagne_voter'),
    url(r'^campagne/resultats/$', 'resultats', name='campagne_resultats'),
    url(r'^palums/json/$', 'palums_json', name='palums_json'),
    url(r'^palums/$', 'palums', name='palums'),
  )
