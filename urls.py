from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
import os

admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^static/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')}),
        
    (r'^admin/?', include(admin.site.urls)),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^accounts/profile/$', 'trombi.views.profile'),
    (r'^sso/1y1b/authentication$', '1y1b.views.connection'),
    (r'^sso/1y1b/logout$', '1y1b.views.logout_view'),
    #(r'^yearbook/$', '1y1b.views.yearbook'),
    (r'^token/$', 'trombi.views.token'),
    (r'^comments/post/$', 'messages.views.post_comment' ),
    (r'^comments/delete/$', 'messages.views.delete_own_comment' ),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^faq/', include('faq.urls')),
    (r'^people/', include('trombi.urls')),
    (r'^messages/', include('messages.urls')),
    (r'^sondages/', include('sondages.urls')),
    (r'^timetable/', include('timetable.urls')),
    (r'^evenements/', include('evenement.urls')),
    (r'^entreprises/', include('entreprise.urls')),
    (r'^petitscours/', include('petitscours.urls')),
    (r'^associations/', include('association.urls')),
    (r'^objetstrouves/?$','objettrouve.views.index'),
    (r'^objetstrouves/ajouter/?$','objettrouve.views.ajouter'),
    (r'^objetstrouves/supprimer/?$','objettrouve.views.supprimer'),
    (r'^bilanmandat/', include('bilanmandat.urls')),
    (r'^recherche/?$','recherche.views.search'),    
    (r'^notifications/$', 'notification.views.liste'),
    (r'^notifications/preferences/$', 'notification.views.preferences'),
    (r'^abatage/$', 'abatage.views.archives_visiteur'),
    (r'^chat/', include('chat.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^accueil/?$','faq.views.accueil'),
    (r'^admissibles/?$','faq.views.admissibles'),
    (r'^trombiassos/?$','trombiassos.views.trombi_assos'),
    (r'^rentree/?$','faq.views.rentree'),
    (r'^logement/?$','faq.views.logement'),
    (r'^admis/?$','faq.views.admis'),
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    (r'^/?$','messages.views.index'),
    (r'^2048/',include('2048.urls'))
)

urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)
