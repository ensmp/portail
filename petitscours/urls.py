from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('petitscours.views',
    url(r'^$','index'),
    url(r'^demander/$', 'demander'),    
    url(r'^admin/$','admin'),
    url(r'^admin/archive/(?P<page>\d*)/$','archive'),
    url(r'^admin/give/(?P<id>\d+)/(?P<mineur_login>\w+)/$','give'),
    url(r'^request/(?P<request_id>\d+)/$','add_request'),
    url(r'^json/$','index_json'),
)