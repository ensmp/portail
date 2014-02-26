from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('abatage.views',
    url(r'^$', 'archives', name='abatage'),
    url(r'^archives/$', 'archives', name='abatage_archives'),
    url(r'^archives/json/$', 'archives_json', name='abatage_archives_json'),
)