from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sitebde.views.home', name='home'),
    #(r'^timetable/', include('sitebde.timetable.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/?', include(admin.site.urls)),
    (r'^messages/?$','messages.views.index'),
    (r'^messages/(?P<message_id>\d+)/$', 'messages.views.detail'),
    (r'^messages/(?P<message_id>\d+)/lire/(?P<no_cache>\S+)/$', 'messages.views.lire'),
    (r'^messages/(?P<message_id>\d+)/classer_important/(?P<no_cache>\S+)/$', 'messages.views.classer_important'),
    (r'^messages/(?P<message_id>\d+)/classer_non_important/(?P<no_cache>\S+)/$', 'messages.views.classer_non_important'),
    (r'^messages/tous/$', 'messages.views.tous'),
    (r'^messages/importants/$', 'messages.views.importants'),
    (r'^associations/$', 'association.views.index'),
    (r'^associations/(?P<association_pseudo>\w+)/$', 'association.views.detail'),
    (r'^associations/(?P<association_pseudo>\w+)/ajouter_membre/$', 'association.views.ajouter_membre'),
    (r'^associations/(?P<association_pseudo>\w+)/supprimer_membre/$', 'association.views.supprimer_membre'),
	(r'^associations/(?P<association_pseudo>\w+)/poster_message/$', 'messages.views.nouveau'),
    (r'^people/?$','trombi.views.index'),
    (r'^people/(?P<mineur_login>\w+)/?$','trombi.views.detail'),
    (r'^people/(?P<mineur_login>\w+)/edit/?$','trombi.views.edit'),
    (r'^objetstrouves/?$','objettrouve.views.index'),
    (r'^objetstrouves/ajouter/?$','objettrouve.views.ajouter'),
    (r'^objetstrouves/supprimer/?$','objettrouve.views.supprimer'),
    (r'^petitscours/?$','petitscours.views.index'),
    (r'^petitscours/admin/?$','petitscours.views.admin'),
    (r'^petitscours/admin/archive/(?P<page>\d*)/?$','petitscours.views.archive'),
    (r'^petitscours/admin/add/?$','petitscours.views.add'),
    (r'^petitscours/admin/give/(?P<id>\d+)/(?P<mineur_login>\w+)/?$','petitscours.views.give'),
    (r'^petitscours/request/(?P<request_id>\d+)/?$','petitscours.views.add_request'),
    (r'^recherche/?$','recherche.views.search'),
    (r'^/?$','streamine.views.index'),
    (r'^accounts/profile/$', 'trombi.views.profile'),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    # (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    # (r'^accounts/password/reset/?$', 'django.contrib.auth.views.password_reset'),

)