from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('messages.views',
    url(r'^$', 'index'),
    url(r'^json/$','index_json'),
    url(r'^tous/$', 'tous'),
    url(r'^tous/json/$', 'tous_json'),
    url(r'^importants/$', 'importants'),
    url(r'^(?P<message_id>\d+)/$', 'detail'),
    url(r'^(?P<message_id>\d+)/edit/$', 'edit'),
    url(r'^(?P<message_id>\d+)/lire/$', 'lire'),
    url(r'^(?P<message_id>\d+)/classer_non_lu/$', 'classer_non_lu'),
    url(r'^(?P<message_id>\d+)/classer_important/$', 'classer_important'),
    url(r'^(?P<message_id>\d+)/classer_non_important/$', 'classer_non_important'),
    url(r'^(?P<message_id>\d+)/supprimer/$', 'supprimer'),
)