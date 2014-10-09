# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from objettrouve.models import ObjetTrouve, ObjetAjoutForm, ObjetSuppressionForm
from django.http import HttpResponseRedirect



@login_required
#La liste des objets perdus/trouv�s
def index(request):
	liste_objets_trouves = ObjetTrouve.objects.filter(trouve=True).order_by('-date')
	liste_objets_perdus = ObjetTrouve.objects.filter(trouve=False).order_by('-date')
	return render_to_response('objettrouve/index.html', {'liste_objets_trouves': liste_objets_trouves,'liste_objets_perdus': liste_objets_perdus},context_instance=RequestContext(request))


@login_required
#Ajouter un nouvel objet perdu/trouv�
def ajouter(request):
	if request.method == 'POST':
		form = ObjetAjoutForm(request.POST)
		if form.is_valid():
			elev = request.user.get_profile()
			desc = form.cleaned_data['description']
			trouv = form.cleaned_data['trouve']
			dat = form.cleaned_data['date']
			lie = form.cleaned_data['lieu']
			ObjetTrouve.objects.create(eleve=elev, trouve = trouv, description=desc, date=dat, lieu=lie)
			return HttpResponseRedirect('/objetstrouves/')
	else:
		form = ObjetAjoutForm()

	return render_to_response('objettrouve/form.html', {'form': form,},context_instance=RequestContext(request))


@login_required
#Supprimer un objet perdu/trouve
def supprimer(request):
	if request.method == 'POST':
		form = ObjetSuppressionForm(request.user, request.POST)
		if form.is_valid():
			objet = form.cleaned_data['objettrouve']
			if ObjetTrouve.objects.filter(id=objet.id, eleve=request.user).exists():
				ObjetTrouve.objects.filter(id=objet.id, eleve=request.user).delete()
			return HttpResponseRedirect('/objetstrouves/')
	else:
		form = ObjetSuppressionForm(request.user)
		#form = ObjetSuppressionForm()

	return render_to_response('objettrouve/form.html', {'form': form,},context_instance=RequestContext(request))
