from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('S3.views',
	url(r'^$', 'newsletter', name='newsletter'),
    url(r'^newsletter/$', 'newsletter', name='newsletter'),
    url(r'^newsletter/json/$', 'newsletter', name='newsletter_json'),
    )