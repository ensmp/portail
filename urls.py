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
    (r'^token/$','trombi.views.token'),
    (r'^messages/$','messages.views.index'),
    (r'^messages/json/$','messages.views.index_json'),
    (r'^messages/(?P<message_id>\d+)/$', 'messages.views.detail'),
    (r'^messages/(?P<message_id>\d+)/edit/$', 'messages.views.edit'),
    (r'^messages/(?P<message_id>\d+)/lire/$', 'messages.views.lire'),
    (r'^messages/(?P<message_id>\d+)/classer_non_lu/$', 'messages.views.classer_non_lu'),
    (r'^messages/(?P<message_id>\d+)/classer_important/$', 'messages.views.classer_important'),
    (r'^messages/(?P<message_id>\d+)/classer_non_important/$', 'messages.views.classer_non_important'),
    (r'^messages/(?P<message_id>\d+)/supprimer/$', 'messages.views.supprimer'),
    (r'^messages/tous/$', 'messages.views.tous'),
    (r'^messages/tous/json/$','messages.views.tous_json'),
    (r'^messages/importants/$', 'messages.views.importants'),
    (r'^evenements/(?P<evenement_id>\d+)/supprimer/$', 'evenement.views.supprimer'),
    (r'^associations/mediamines/', include('mediamines.urls')),
    (r'^associations/minesmarket/catalogue/$','minesmarket.views.catalogue'),
    (r'^associations/minesmarket/commande/$','minesmarket.views.commande'),
    (r'^associations/minesmarket/acheter/$','minesmarket.views.acheter'),
    (r'^associations/minesmarket/supprimer_achat/(?P<id_achat>\d+)/$','minesmarket.views.supprimer_achat'),
    (r'^associations/minesmarket/supprimer_tous_achats/$','minesmarket.views.supprimer_tous_achats'),
    (r'^associations/minesmarket/fermer_commandes/$','minesmarket.views.fermer_commandes'),
    (r'^associations/minesmarket/dernieres_commandes/$','minesmarket.views.dernieres_commandes_csv'),
    (r'^associations/trium/informations/$', TemplateView.as_view(template_name='trium/informations.html')),
    (r'^associations/jump/etudes/$', 'jump.views.etudes'),
    (r'^associations/minestryofsound/nouveau/$','minestryofsound.views.nouveau'),
    (r'^associations/minestryofsound/playlist/$','minestryofsound.views.playlist'),
    (r'^associations/minestryofsound/playlist/json/$','minestryofsound.views.playlist_json'),
    (r'^associations/minestryofsound/player/playlist.xml$','minestryofsound.views.playlist_xml'),
    (r'^associations/minestryofsound/player/$','minestryofsound.views.playlist_popup'),
    (r'^associations/vendome/',include('vendome.urls')),    
    (r'^abatage/$','abatage.views.archives_visiteur'),
    (r'^associations/abatage/$','abatage.views.archives'),    
    (r'^associations/abatage/archives/$','abatage.views.archives'),
    (r'^associations/abatage/archives/json/$','abatage.views.archives_json'),
    (r'^associations/mds/zezinho/$',TemplateView.as_view(template_name='mds/zezinho.html')),
    (r'^associations/vp/destinations/$',TemplateView.as_view(template_name='voyagepromo/destinations.html')),
    (r'^associations/vp/destinations/cuba/$',TemplateView.as_view(template_name='voyagepromo/cuba.html')),
    (r'^associations/vp/destinations/bali/$',TemplateView.as_view(template_name='voyagepromo/bali.html')),
    (r'^associations/vp/destinations/mexique/$',TemplateView.as_view(template_name='voyagepromo/mexique.html')),
    (r'^associations/pr/clips/$', 'pr.views.clips'),
    (r'^associations/bde/', include('bde.urls')),
    (r'^associations/wei/teaser/$',TemplateView.as_view(template_name='wei/teaser.html')),
    (r'^associations/(?P<association_pseudo>\w+)/$', 'association.views.messages'),
    (r'^associations/(?P<association_pseudo>\w+)/equipe/$', 'association.views.equipe'),
    (r'^associations/(?P<association_pseudo>\w+)/equipe/changer_ordre/$', 'association.views.changer_ordre'),    
    (r'^associations/(?P<association_pseudo>\w+)/equipe/ajouter_membre/$', 'association.views.ajouter_membre'),
    (r'^associations/(?P<association_pseudo>\w+)/equipe/supprimer_membre/$', 'association.views.supprimer_membre'),
    (r'^associations/(?P<association_pseudo>\w+)/messages/$', 'association.views.messages'),
    (r'^associations/(?P<association_pseudo>\w+)/messages/poster_message/$', 'messages.views.nouveau'),
    (r'^associations/(?P<association_pseudo>\w+)/evenements/$', 'association.views.evenements'),
    (r'^associations/(?P<association_pseudo>\w+)/evenements/nouveau/$', 'evenement.views.nouveau'),
    (r'^associations/(?P<association_pseudo>\w+)/medias/affiche/ajouter/$', 'association.views.ajouter_affiche'),
    (r'^associations/(?P<association_pseudo>\w+)/medias/affiche/(?P<affiche_id>\d+)/supprimer/$', 'association.views.supprimer_affiche'),
    (r'^associations/(?P<association_pseudo>\w+)/medias/video/ajouter/$', 'association.views.ajouter_video'),
    (r'^associations/(?P<association_pseudo>\w+)/medias/video/(?P<video_id>\d+)/supprimer/$', 'association.views.supprimer_video'),
    (r'^associations/(?P<association_pseudo>\w+)/medias/$', 'association.views.medias'),  
    (r'^associations/$', 'association.views.index'),    
    (r'^people/$','trombi.views.trombi'),
    (r'^people/octo_update/$','trombi.views.octo_update'),
    (r'^people/avatar/', include('avatar.urls')),    
    (r'^people/json/$','trombi.views.trombi_json'),
    (r'^people/separation/mine/$',TemplateView.as_view(template_name='trombi/graphe-mine.html')),
    (r'^people/separation/graphe/$','trombi.views.separation_graphe'),
    (r'^people/separation/$','trombi.views.separation'),
    (r'^people/(?P<mineur_login>\w+)/?$','trombi.views.detail'),
    (r'^people/(?P<mineur_login>\w+)/json/$','trombi.views.detail_json'),
    (r'^people/(?P<mineur_login>\w+)/edit/?$','trombi.views.edit'),   
    (r'^people/trombi.vcf$','trombi.views.get_vcf'), 
    (r'^evenements/', include('evenement.urls')),
    (r'^timetable/', include('timetable.urls')),
    (r'^objetstrouves/?$','objettrouve.views.index'),
    (r'^objetstrouves/ajouter/?$','objettrouve.views.ajouter'),
    (r'^objetstrouves/supprimer/?$','objettrouve.views.supprimer'),
    (r'^petitscours/?$','petitscours.views.index'),
    (r'^petitscours/demander/', 'petitscours.views.demander'),    
    (r'^petitscours/admin/?$','petitscours.views.admin'),
    (r'^petitscours/admin/archive/(?P<page>\d*)/?$','petitscours.views.archive'),
    # (r'^petitscours/add/?$','petitscours.views.add'),
    (r'^petitscours/admin/give/(?P<id>\d+)/(?P<mineur_login>\w+)/?$','petitscours.views.give'),
    (r'^petitscours/request/(?P<request_id>\d+)/?$','petitscours.views.add_request'),
    (r'^petitscours/json/?$','petitscours.views.index_json'),
    (r'^todo/nouveau/?$','todo.views.nouveau'),
    (r'^todo/(?P<id_note>\d+)/supprimer/?$','todo.views.supprimer'),
    (r'^sondages/voter/?$','sondages.views.voter'),
    (r'^sondages/scores/?$','sondages.views.scores'),
    (r'^sondages/proposer/?$','sondages.views.proposer'),
    (r'^sondages/valider/?$','sondages.views.valider'),
    (r'^sondages/en-attente/?$','sondages.views.en_attente'),
    (r'^sondages/supprimer/?$','sondages.views.supprimer'),
    (r'^sondages/(?P<indice_sondage>\d+)/json/?$','sondages.views.detail_json'),    
    (r'^recherche/?$','recherche.views.search'),    
    (r'^accounts/profile/$', 'trombi.views.profile'),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^comments/post/$', 'messages.views.post_comment' ),
    (r'^comments/delete/$', 'messages.views.delete_own_comment' ),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^notifications/$', 'notification.views.liste'),
    (r'^notifications/preferences/$', 'notification.views.preferences'),
    (r'^faq/$', 'faq.views.questions'),
    (r'^faq/question_posee/?$','faq.views.question_posee'),
	(r'^faq/poser_question/?$','faq.views.poser_question'),
    (r'^entreprises/$','entreprise.views.presentation_entreprises'),
    (r'^entreprises/contact/$','entreprise.views.contact_entreprises'),
    (r'^entreprises/planning/$','entreprise.views.planning'),
    (r'^entreprise/$', 'entreprise.views.index'),  
    (r'^chat/', include('chat.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    # (r'^online/', include('online_status.urls')), 
    (r'^accueil/?$','faq.views.accueil'),
    (r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt')),
    (r'^/?$','messages.views.index'),
)

urlpatterns += patterns('', url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,}),)
