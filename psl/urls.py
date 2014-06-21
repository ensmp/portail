from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('psl.views',
	url(r'^$', 'archives', name='newsletter'),
    url(r'^archives/$', 'archives', name='newsletter_archives'),
    url(r'^archives/json/$', 'archives_json', name='newsletter_archives_json'),
    )