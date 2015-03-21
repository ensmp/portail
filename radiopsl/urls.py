from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('radiopsl.views',
	url(r'^$', 'lecteur', name='lecteur'),
    url(r'^lecteur/$', 'lecteur', name='lecteur'),
    )