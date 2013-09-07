from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('bde.views',
    url(r'^archives_palum/json/$', 'archives_palum', name='archives_palum_json'),
    url(r'^archives_palum/$', 'archives_palum', name='archives_palum'),
    url(r'^voter/$', 'voter', name='voter'),
    url(r'^resultats/$', 'resultats', name='resultats'),
  )
