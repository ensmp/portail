from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('pr.views',
    url(r'^voter/$', 'voter', name='voter'),
    url(r'^resultats/$', 'resultats', name='resultats'),
    url(r'^clips/$', 'clips', name='clips'),
    url(r'^export_votes/$', 'voir_votes_csv')
  )

