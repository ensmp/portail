from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from association.models import Association, Adhesion, AdhesionAjoutForm, AdhesionSuppressionForm
from trombi.models import UserProfile
from messages.models import Message
from evenement.models import Evenement, Billetterie

@login_required
def index(request):
	liste_evenements = Evenement.objects.all().order_by('date_debut')
	return render_to_response('evenement/calendrier.html', {'liste_evenements':liste_evenements},context_instance=RequestContext(request))
	

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