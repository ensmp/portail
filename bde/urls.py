from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bde.views',
    url(r'^palums/json/$', 'palums_json', name='palums_json'),
    url(r'^palums/$', 'palums', name='palums'),
    url(r'^voter/$', 'voter', name='voter'),
    url(r'^resultats/$', 'resultats', name='resultats'),
  )
