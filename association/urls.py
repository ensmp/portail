#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

# Views d'autres modules
urlpatterns = patterns('',
    url(r'^(?P<association_pseudo>\w+)/messages/poster_message/$', 'messages.views.nouveau'),
    url(r'^(?P<association_pseudo>\w+)/evenements/nouveau/$', 'evenement.views.nouveau'),
    url(r'^trium/informations/$', TemplateView.as_view(template_name='trium/informations.html')),
    url(r'^wei/teaser/$', TemplateView.as_view(template_name='wei/teaser.html')),
    url(r'^minestryofsound/', include('minestryofsound.urls')),
    url(r'^minesmarket/', include('minesmarket.urls')),
    url(r'^freshbox/', include('freshbox.urls')),
    url(r'^mediamines/', include('mediamines.urls')),
    url(r'^paindemine/', include('paindemine.urls')),
    url(r'^abatage/', include('abatage.urls')),
    url(r'^vendome/', include('vendome.urls')),
    url(r'^bde/', include('bde.urls')),
    url(r'^bda/', include('bda.urls')),
    url(r'^htc/', include('htc.urls')),
    url(r'^psl/', include('psl.urls')),
    url(r'^pr/', include('pr.urls')),
    url(r'^mineshake/', include('mineshake.urls')),
    url(r'^S3/', include('S3.urls')),
    url(r'^radiopsl/', include('radiopsl.urls')),
)

# Views du module association
urlpatterns += patterns('association.views',
    url(r'^$', 'index', name='associations'),
    url(r'^(?P<association_pseudo>\w+)/$', 'messages'),
    url(r'^(?P<association_pseudo>\w+)/equipe/$', 'equipe'),
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_ordre/$', 'changer_ordre'),    
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_role/(?P<eleve_id>\d+)$', 'changer_role'),    
    url(r'^(?P<association_pseudo>\w+)/equipe/changer_role/$', 'changer_role', {'eleve_id':None}),    
    url(r'^(?P<association_pseudo>\w+)/equipe/ajouter_membre/$', 'ajouter_membre'),
    url(r'^(?P<association_pseudo>\w+)/equipe/supprimer_membre/$', 'supprimer_membre'),
    url(r'^(?P<association_pseudo>\w+)/messages/$', 'messages'),
    url(r'^(?P<association_pseudo>\w+)/evenements/$', 'evenements'),
    url(r'^(?P<association_pseudo>\w+)/medias/$', 'medias', name='association_medias'),
    url(r'^(?P<association_pseudo>\w+)/medias/video/ajouter/$', 'ajouter_video'),
    url(r'^(?P<association_pseudo>\w+)/medias/video/(?P<video_id>\d+)/supprimer/$', 'supprimer_video'),
    url(r'^(?P<association_pseudo>\w+)/medias/affiche/ajouter/$', 'ajouter_affiche'),
    url(r'^(?P<association_pseudo>\w+)/medias/affiche/(?P<affiche_id>\d+)/supprimer/$', 'supprimer_affiche'),
)
