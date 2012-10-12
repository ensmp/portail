#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from association.models import Association, Adhesion, AdhesionAjoutForm, AdhesionSuppressionForm
from trombi.models import UserProfile
from messages.models import Message
from evenement.models import Evenement
from django.http import Http404, HttpResponse, HttpResponseRedirect
from datetime import date, datetime, timedelta
from django.db.models import Q

import json


@login_required
#Le calendrier. Les évenements sont chargés depuis la vue index_json.
def index(request):
	return render_to_response('evenement/calendrier.html', {},context_instance=RequestContext(request))

@login_required	
#La serialisation des évenements au format JSON. Pour l'affichage dans le calendrier, et sur les applis.
def index_json(request):
	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None #pour le formatage des dates
	evenement_list = Evenement.objects.exclude(Q(is_personnel=True) & ~Q(createur__user__username=request.user.username)) #On ne lit pas les evenements personnels d'autrui.
	response = HttpResponse(mimetype='application/json')
	response.write(json.dumps([{
			'id': e.id,
			'auteur': e.auteur(),
			'start': e.date_debut,
			'end': e.date_fin,
			'title': e.titre, 	
			'body': e.description, 
			'readOnly':not(e.peut_modifier(request.user)) #Lecture seule si on n'est pas autorisé à le modifier
		} for e in evenement_list], default=dthandler))
	return response

@login_required
#Création d'un nouvel évenement, depuis le calendrier.
def nouveau_calendrier(request): 
	debut = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_debut']), int(request.POST['minutes_debut']))
	fin = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_fin']), int(request.POST['minutes_fin']))
	
	if fin < debut: #si l'heure de fin est avant l'heure de debut, c'est que ca termine le lendemain
		fin = fin + timedelta(days=1)

	Evenement.objects.create(association = None, createur = request.user.get_profile(), titre = request.POST['title'], description = request.POST['body'], date_debut = debut, date_fin=fin, is_billetterie = False, is_personnel = True)
	
	return HttpResponse('Ok (ajout)')

@login_required	
#Suppression d'un évenement, depuis le calendrier.
def supprimer_calendrier(request):
	evenement = Evenement.objects.get(pk=request.POST['id'])
	if evenement.peut_modifier(request.user):
		evenement.delete()
	return HttpResponse('Ok (suppression)')

@login_required	
#Suppression d'un évenement
def supprimer(request, evenement_id):
	evenement = Evenement.objects.get(pk=evenement_id)
	association = evenement.association
	if evenement.peut_modifier(request.user):
		evenement.delete()
	return HttpResponseRedirect(association.get_absolute_url() + 'evenements/')

	
@login_required	
#Mise à jour d'un évenement, depuis le calendrier.
def update_calendrier(request):	
	evenement = Evenement.objects.get(pk=request.POST['id'])
	if evenement.peut_modifier(request.user):
		debut = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_debut']), int(request.POST['minutes_debut']))
		fin = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_fin']), int(request.POST['minutes_fin']))
		evenement.titre = request.POST['title']
		evenement.description = request.POST['body']
		evenement.date_debut = debut
		evenement.date_fin=fin
		evenement.save()
	return HttpResponse('Ok (update)')	

@login_required
#Création d'un nouvel évenement, depuis la page "évenements" d'une association
def nouveau(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	if request.POST:
		debut = datetime(int(str(request.POST['date'])[6:10]), int(str(request.POST['date'])[3:5]), int(str(request.POST['date'])[0:2]), int(str(request.POST['debut'])[0:2]), int(str(request.POST['debut'])[3:5]))
		fin = datetime(int(str(request.POST['date'])[6:10]), int(str(request.POST['date'])[3:5]), int(str(request.POST['date'])[0:2]), int(str(request.POST['fin'])[0:2]), int(str(request.POST['fin'])[3:5]))
		
		if fin < debut: #si l'heure de fin est avant l'heure de debut, c'est que ca termine le lendemain
			fin = fin + timedelta(days=1)
		
		if Adhesion.objects.filter(association=association, eleve=request.user).exists():
			Evenement.objects.create(association = association, createur = request.user.get_profile(), titre = request.POST['titre'], description = request.POST['description'], lieu =request.POST['lieu'], date_debut = debut, date_fin=fin, is_billetterie = False, is_personnel = False)
		return HttpResponseRedirect('/associations/'+association_pseudo+'/evenements/')
	else:
		return render_to_response('evenement/nouveau.html', {'association' : association},context_instance=RequestContext(request))
	

@login_required
def confirmer_billetterie(request, association_pseudo, evenement_id):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	evenement = get_object_or_404(Evenement, pk=evenement_id)
	evenement.participants.add(request.user.get_profile())
	evenement.save()
	return render_to_response('messages/action.html', {'association' : association},context_instance=RequestContext(request))

@login_required
def consulter_billetterie(request, association_pseudo, evenement_id):	
	association = get_object_or_404(Association,pseudo=association_pseudo)
	evenement = get_object_or_404(Evenement, pk=evenement_id)
	liste_billetterie = Evenement.objects.filter(participants__user__username=request.user.username).order_by('-date_debut')
	return render_to_response('evenement/billetterie.html', {'association' : association, 'evenement' : evenement, 'liste_billetterie' : liste_billetterie},context_instance=RequestContext(request))
	
@login_required
def billetterie_globale (request):
	liste_billetterie = Evenement.objects.filter(participants__user__username=request.user.username).order_by('-date_debut')
	return render_to_response('evenement/billetterie.html', {'liste_billetterie' : liste_billetterie},context_instance=RequestContext(request))
