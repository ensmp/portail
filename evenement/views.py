from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from association.models import Association, Adhesion, AdhesionAjoutForm, AdhesionSuppressionForm
from trombi.models import UserProfile
from messages.models import Message
from evenement.models import Evenement, Billetterie
from django.http import Http404, HttpResponse
from datetime import date, datetime, timedelta
import json


@login_required
def index(request):
	liste_evenements = Evenement.objects.all().order_by('date_debut')
	return render_to_response('evenement/calendrier.html', {'liste_evenements':liste_evenements},context_instance=RequestContext(request))

@login_required	
def index_json(request):
	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
	evenement_list = Evenement.objects.all()
	response = HttpResponse(mimetype='application/json')
	response.write(json.dumps([{
			'id': e.id,
			'auteur': e.auteur(),
			'start': e.date_debut,
			'end': e.date_fin,
			'title': e.titre, 	
			'body': e.description, 
			'readOnly':not(e.peut_modifier(request.user))
		} for e in evenement_list], default=dthandler))
	return response

@login_required
def nouveau_calendrier(request):
	debut = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_debut']), int(request.POST['minutes_debut']))
	fin = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_fin']), int(request.POST['minutes_fin']))
	
	Evenement.objects.create(association = None, createur = request.user.get_profile(), titre = request.POST['title'], description = request.POST['body'], date_debut = debut, date_fin=fin, is_billetterie = False)
	
	return HttpResponse('Ok (ajout)')

@login_required	
def supprimer_calendrier(request):	
	evenement = Evenement.objects.get(pk=request.POST['id'])
	if evenement.peut_modifier(request.user):
		evenement.delete()
	return HttpResponse('Ok (suppression)')

@login_required	
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
	

def billetterie_globale (request):
	liste_billetterie = Evenement.objects.filter(participants__user__username=request.user.username).order_by('-date_debut')
	return render_to_response('evenement/billetterie.html', {'liste_billetterie' : liste_billetterie},context_instance=RequestContext(request))
