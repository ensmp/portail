from association.models import Association, Adhesion, AdhesionAjoutForm, AdhesionSuppressionForm
from trombi.models import UserProfile
from messages.models import Message
from evenement.models import Evenement
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q


# Create your views here.
@login_required
def index(request):
	assoces = Association.objects.all();
	return render_to_response('association/index.html', {'assoces' : assoces},context_instance=RequestContext(request))

@login_required
def equipe(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('eleve__user__username')

	return render_to_response('association/equipe.html', {'association' : association, 'membres': membres},context_instance=RequestContext(request))

@login_required
def messages(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	list_messages = Message.objects.filter(association__pseudo=association_pseudo).filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all())).order_by('-date')

	return render_to_response('association/messages.html', {'association' : association, 'list_messages': list_messages},context_instance=RequestContext(request))
#view evenement ajoutee	
@login_required
def evenements(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	list_evenements = Evenement.objects.filter(association__pseudo=association_pseudo).order_by('-date')

	return render_to_response('association/evenements.html', {'association' : association, 'list_evenements': list_evenements},context_instance=RequestContext(request))
	#
@login_required	
def ajouter_membre(request, association_pseudo):
	assoce = get_object_or_404(Association,pseudo=association_pseudo)
	if request.method == 'POST': # If the form has been submitted...
		form = AdhesionAjoutForm(assoce, request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			utilisateur = form.cleaned_data['eleve']
			fonction = form.cleaned_data['role']
			if Adhesion.objects.filter(association=assoce, eleve=request.user).exists():
				Adhesion.objects.create(eleve=utilisateur, association=assoce, role=fonction)
			return HttpResponseRedirect('/associations/'+assoce.pseudo) # Redirect after POST
	else:
		form = AdhesionAjoutForm(assoce) # An unbound form

	return render_to_response('association/admin.html', {'form': form,},context_instance=RequestContext(request))
	
	
@login_required	
def supprimer_membre(request, association_pseudo):
	assoce = get_object_or_404(Association,pseudo=association_pseudo)
	if request.method == 'POST': # If the form has been submitted...
		form = AdhesionSuppressionForm(assoce, request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			utilisateur = form.cleaned_data['eleve']
			if Adhesion.objects.filter(association=assoce, eleve=request.user).exists():
				Adhesion.objects.filter(eleve=utilisateur, association=assoce).delete()
			return HttpResponseRedirect('/associations/'+assoce.pseudo) # Redirect after POST
	else:
		form = AdhesionSuppressionForm(assoce) # An unbound form

	return render_to_response('association/admin.html', {'form': form,},context_instance=RequestContext(request))
	
	