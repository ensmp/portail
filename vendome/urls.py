from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('vendome.views',
    url(r'^$', 'archives', name='vendome'),
    url(r'^archives/$', 'archives', name='vendome_archives'),
    url(r'^archives/json/$', 'archives_json', name='vendome_archives_json'),
)