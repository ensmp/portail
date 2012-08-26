#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from sondages.models import Sondage, Vote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required

import json
import datetime


@login_required
def voter(request):
	if Sondage.objects.filter(deja_paru = False, date_parution = datetime.date.today()).exists(): #Le sondage du jour a déjà été choisi
		sondage = get_object_or_404(Sondage, deja_paru = False, date_parution = datetime.date.today()) #On le récupère
		if Vote.objects.filter(sondage = sondage, eleve__user__username=request.user.username).exists(): #L'élève a déjà voté
			messages.add_message(request, messages.ERROR, "Vous avez déjà voté pour ce sondage")
		else:
			if request.POST['choix']:				
				Vote.objects.create(sondage = sondage, eleve=request.user.get_profile(), choix = int(request.POST['choix']))
				messages.add_message(request, messages.INFO, "A voté !")
	if request.POST['next']:
		return HttpResponseRedirect(request.POST['next'])
	else:
		return HttpResponseRedirect('/')
	#return render_to_response('messages/action.html', {},context_instance=RequestContext(request))
	
@login_required
def proposer(request):
	if request.POST:
		if request.POST['question'] and request.POST['reponse1'] and request.POST['reponse2']:
			sondage = Sondage(auteur = request.user.get_profile(), question = request.POST['question'], reponse1 = request.POST['reponse1'], reponse2 = request.POST['reponse2'])
			sondage.save()
			sondage.envoyer_notification()
			messages.add_message(request, messages.INFO, "Votre sondage a bien été enregistré, il est maintenant en attente de validation.")			
		else:
			messages.add_message(request, messages.ERROR, "Vous devez spécifier une question et deux réponses.")
		return HttpResponseRedirect('/sondages/proposer/')
	else:
		return render_to_response('sondages/proposer.html',{},context_instance=RequestContext(request))


@permission_required('sondages.add_sondage')
def valider(request):
	if request.POST:
		sondage = get_object_or_404(Sondage, pk=request.POST['id'])
		sondage.autorise = True
		sondage.save()
		messages.add_message(request, messages.INFO, "Sondage validé")
		return HttpResponseRedirect('/sondages/valider/')
	else:
		liste_sondages = Sondage.objects.filter(autorise = False)
		return render_to_response('sondages/valider.html',{'liste_sondages':liste_sondages},context_instance=RequestContext(request))

@permission_required('sondages.delete_sondage')
def supprimer(request):
	if request.POST:
		sondage = get_object_or_404(Sondage, pk=request.POST['id'])		
		sondage.delete()
		messages.add_message(request, messages.INFO, "Sondage supprimé")
	return HttpResponseRedirect('/sondages/valider/')
	
@login_required	
def detail_json(request, indice_sondage):
	sondage = Sondage.objects.filter(date_parution__isnull = False).filter(date_parution__lte = datetime.date.today()).order_by('-date_parution')[int(indice_sondage)]
	nombre_reponse = Vote.objects.filter(sondage = sondage).count()
	nombre_reponse_1 = Vote.objects.filter(sondage = sondage, choix = 1).count()
	nombre_reponse_2 = Vote.objects.filter(sondage = sondage, choix = 2).count()
	response = HttpResponse(mimetype='application/json')
	response.write(json.dumps({
			'question': sondage.question,
			'reponse1': sondage.reponse1,
			'reponse2': sondage.reponse2,
			'nombre_reponse': nombre_reponse,
			'nombre_reponse_1': nombre_reponse_1,
			'nombre_reponse_2': nombre_reponse_2,
			'date_parution': sondage.date_str()
		}))
	return response