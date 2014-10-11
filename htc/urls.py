from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('HTC.views',
	url(r'^$', 'newsletter', name='newsletter'),
    url(r'^newsletter/$', 'newsletter', name='newsletter'),
    url(r'^newsletter/json/$', 'newsletter', name='newsletter_json'),
    )