from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('2048.views',
    url(r'^2048/$', 'page2048'),
    url(r'^2048/givescore', 'givescore'),
)