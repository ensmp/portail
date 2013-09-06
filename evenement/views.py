#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from association.models import Association, Adhesion
from evenement.models import Evenement
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.contrib import messages
import json

@login_required
def index(request):
	"""Le calendrier. Les évenements sont chargés depuis la vue index_json."""
	return render_to_response('evenement/calendrier.html', {},context_instance=RequestContext(request))

@login_required	
def index_json(request):
	"""Sérialiser les évenements au format JSON. Pour l'affichage dans le calendrier et sur les applis mobiles."""
	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None #pour le formatage des dates
	evenement_list = Evenement.objects.all()
	response = HttpResponse(mimetype='application/json')
	response.write(json.dumps([{
			'id': e.id,
			'auteur': e.auteur(),
			'auteur_slug' : e.auteur_slug(),
			'start': e.date_debut,
			'end': e.date_fin,
			'title': e.titre, 	
			'body': e.description, 
			'readOnly':not(e.peut_modifier(request.user)) # Lecture seule si on n'est pas autorisé à le modifier
		} for e in evenement_list], default=dthandler))
	return response

@login_required
def nouveau_calendrier(request): 
	"""Créer un nouvel évenement, depuis le calendrier."""
	debut = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_debut']), int(request.POST['minutes_debut']))
	fin = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_fin']), int(request.POST['minutes_fin']))
	
	if fin < debut: # Si l'heure de fin est avant l'heure de debut, c'est que ca termine le lendemain
		fin = fin + timedelta(days=1)

	Evenement.objects.create(association = None, createur = request.user.get_profile(), titre = request.POST['title'], description = request.POST['body'], date_debut = debut, date_fin = fin)
	
	return HttpResponse('Ok (ajout)')

@login_required	
def supprimer_calendrier(request):
	"""Supprimer un évenement, depuis le calendrier."""
	evenement = Evenement.objects.get(pk=request.POST['id'])
	if evenement.peut_modifier(request.user):
		evenement.delete()
	return HttpResponse('Ok (suppression)')

	
@login_required	
def update_calendrier(request):	
	"""Mettre à jour un évenement, depuis le calendrier."""
	evenement = Evenement.objects.get(pk=request.POST['id'])
	if evenement.peut_modifier(request.user):
		debut = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_debut']), int(request.POST['minutes_debut']))
		fin = datetime(int(request.POST['annee']), int(request.POST['mois'])+1, int(request.POST['jour']), int(request.POST['heures_fin']), int(request.POST['minutes_fin']))
		evenement.titre = request.POST['title']
		evenement.description = request.POST['body']
		evenement.date_debut = debut
		evenement.date_fin = fin
		evenement.save()
	return HttpResponse('Ok (update)')	

@login_required
def nouveau(request, association_pseudo):
	"""Créer un nouvel événement"""
	association = get_object_or_404(Association,pseudo=association_pseudo)
	if request.POST:
		debut = datetime(int(str(request.POST['date'])[6:10]), int(str(request.POST['date'])[3:5]), int(str(request.POST['date'])[0:2]), int(str(request.POST['debut'])[0:2]), int(str(request.POST['debut'])[3:5]))
		fin = datetime(int(str(request.POST['date'])[6:10]), int(str(request.POST['date'])[3:5]), int(str(request.POST['date'])[0:2]), int(str(request.POST['fin'])[0:2]), int(str(request.POST['fin'])[3:5]))
		
		if fin < debut: # Si l'heure de fin est avant l'heure de debut, c'est que ca termine le lendemain
			fin = fin + timedelta(days=1)
		
		if Adhesion.existe(request.user.get_profile(), association):
			evenement = Evenement.objects.create(association = association, createur = request.user.get_profile(), titre = request.POST['titre'], description = request.POST['description'], lieu =request.POST['lieu'], date_debut = debut, date_fin=fin)
			messages.add_message(request, messages.SUCCESS, "Evénement ajouté !")
			return redirect(evenement.get_absolute_url())
		else:
			messages.add_message(request, messages.SUCCESS, "Vous n'avez pas la permission !")
			return redirect(association.get_absolute_url() + 'evenements/')
	else:
		return render_to_response('evenement/nouveau.html', {'association' : association}, context_instance=RequestContext(request))

@login_required
def supprimer(request, evenement_id):
    """Supprimer un événement"""
    evenement = get_object_or_404(Evenement, pk = evenement_id)
    association = evenement.association
    if Adhesion.existe(request.user.get_profile(), association):
        evenement.delete()
        messages.add_message(request, messages.SUCCESS, "Evénement supprimé !")
    return redirect(association.get_absolute_url() + 'evenements/')