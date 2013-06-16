#-*- coding: utf-8 -*-
from association.models import Association, Adhesion, Affiche, Video, AdhesionAjoutForm, AdhesionSuppressionForm, AfficheForm, VideoForm
from trombi.models import UserProfile
from messages.models import Message
from evenement.models import Evenement
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q


@login_required
# La liste de toutes les associations
def index(request):
    assoces = Association.objects.order_by('ordre');
    return render_to_response('association/index.html', {'assoces' : assoces},context_instance=RequestContext(request))

@login_required
# La liste des membres d'une association
def equipe(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    return render_to_response('association/equipe.html', {'association' : association, 'membres': membres},context_instance=RequestContext(request))

@login_required
# Les messages postés par une association
def messages(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    list_messages = Message.objects.filter(association__pseudo=association_pseudo).order_by('-date')
    return render_to_response('association/messages.html', {'association' : association, 'list_messages': list_messages, 'membres': membres},context_instance=RequestContext(request))

@login_required
# Les événements planifiés par une association
def evenements(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    liste_evenements = Evenement.objects.filter(association__pseudo=association_pseudo).order_by('-date_debut')

    return render_to_response('association/evenements.html', {'association' : association, 'liste_evenements': liste_evenements, 'membres': membres},context_instance=RequestContext(request))

@login_required
# Les événements planifiés par une association
def medias(request, association_pseudo):
    association = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    liste_affiches = Affiche.objects.filter(association__pseudo=association_pseudo)
    liste_videos = Video.objects.filter(association__pseudo=association_pseudo)

    return render_to_response('association/medias.html', {'association' : association, 'liste_affiches': liste_affiches, 'liste_videos': liste_videos, 'membres': membres},context_instance=RequestContext(request))
    
@login_required    
# Ajouter un membre à une association
def ajouter_membre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    if request.method == 'POST': 
        form = AdhesionAjoutForm(assoce, request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            fonction = form.cleaned_data['role']
            if Adhesion.objects.filter(association=assoce, eleve=request.user).exists(): #Si l'eleve est membre de l'assoce
                Adhesion.objects.create(eleve=utilisateur, association=assoce, role=fonction)
            return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/')
    else:
        form = AdhesionAjoutForm(assoce) # formulaire vierge

    return render_to_response('association/admin.html', {'form': form,},context_instance=RequestContext(request))
    
    
@login_required    
# Supprimer un membre d'une association
def supprimer_membre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    if request.method == 'POST': 
        form = AdhesionSuppressionForm(assoce, request.POST) 
        if form.is_valid(): 
            utilisateur = form.cleaned_data['eleve']
            if Adhesion.objects.filter(association=assoce, eleve=request.user).exists(): #Si l'eleve est membre de l'assoce
                Adhesion.objects.filter(eleve=utilisateur, association=assoce).delete()
            return HttpResponseRedirect('/associations/'+assoce.pseudo)
    else:
        form = AdhesionSuppressionForm(assoce)

    return render_to_response('association/admin.html', {'form': form,},context_instance=RequestContext(request))
    
@login_required    
#Changer l'ordre des élèves dans le trombi d'une association
def changer_ordre(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    nombre_membres = Adhesion.objects.filter(association__pseudo = association_pseudo).count()
    if request.method == 'POST': 
        if Adhesion.objects.filter(association=assoce, eleve=request.user).exists():#Si l'eleve est membre de l'assoce
            for i in range(1,nombre_membres+1):#Boucle sur les eleves
                adhesion = get_object_or_404(Adhesion,eleve__user__username=request.POST['login-'+str(i)], association = assoce)#On recupert l'eleve par son login
                adhesion.ordre = request.POST['position-'+str(i)]#On change sa position
                adhesion.save()
        return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/') 
    return render_to_response('association/ordre.html', {'association':assoce, 'membres': membres, 'indices_membres': range(nombre_membres)},context_instance=RequestContext(request))
    
def ajouter_affiche(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    if request.method == 'POST':
        formset = AfficheForm(request.POST, request.FILES)
        if Adhesion.objects.filter(association=assoce, eleve=request.user).exists():#Si l'eleve est membre de l'assoce
            if formset.is_valid():
                affiche = formset.save(commit=False)
                affiche.association = assoce
                affiche.save()
                return HttpResponseRedirect(assoce.get_absolute_url() + 'medias/')
    else:
        formset = AfficheForm()
    return render_to_response("association/ajouter_affiche.html", {'association':assoce, 'membres': membres,   "formset": formset},context_instance=RequestContext(request))

def supprimer_affiche(request,association_pseudo,affiche_id):
    affiche = get_object_or_404(Affiche,pk=affiche_id)
    association = affiche.association
    if Adhesion.objects.filter(association=association, eleve=request.user).exists():#Si l'eleve est membre de l'assoce
        affiche.delete()
    return HttpResponseRedirect(association.get_absolute_url() + 'medias/')
    
def ajouter_video(request, association_pseudo):
    assoce = get_object_or_404(Association,pseudo=association_pseudo)
    membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
    if request.method == 'POST':
        formset = VideoForm(request.POST, request.FILES)
        if formset.is_valid():
            video = formset.save(commit=False)
            video.association = assoce
            video.save()
            return HttpResponseRedirect(assoce.get_absolute_url() + 'medias/')
    else:
        formset = VideoForm()
    return render_to_response("association/ajouter_video.html", {'association':assoce, 'membres': membres,   "formset": formset},context_instance=RequestContext(request))
    
def supprimer_video(request, association_pseudo, video_id):
    video = get_object_or_404(Video,pk=video_id)
    association = video.association
    if Adhesion.objects.filter(association=association, eleve=request.user).exists():#Si l'eleve est membre de l'assoce
        video.delete()
    return HttpResponseRedirect(association.get_absolute_url() + 'medias/')