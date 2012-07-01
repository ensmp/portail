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
	membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
	return render_to_response('association/equipe.html', {'association' : association, 'membres': membres},context_instance=RequestContext(request))

@login_required
def messages(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
	list_messages = Message.objects.filter(association__pseudo=association_pseudo).filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all())).order_by('-date')
	return render_to_response('association/messages.html', {'association' : association, 'list_messages': list_messages, 'membres': membres},context_instance=RequestContext(request))
#view evenement ajoutee	
@login_required
def evenements(request, association_pseudo):
	association = get_object_or_404(Association,pseudo=association_pseudo)
	liste_evenements = Evenement.objects.filter(association__pseudo=association_pseudo).order_by('-date_debut')

	return render_to_response('association/evenements.html', {'association' : association, 'liste_evenements': liste_evenements},context_instance=RequestContext(request))
	#
@login_required	
def ajouter_membre(request, association_pseudo):
	assoce = get_object_or_404(Association,pseudo=association_pseudo)
	if request.method == 'POST': # If the form has been submitted...
		form = AdhesionAjoutForm(assoce, request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			utilisateur = form.cleaned_data['eleve']
			fonction = form.cleaned_data['role']
			if Adhesion.objects.filter(association=assoce, eleve=request.user).exists(): #Si l'eleve est membre de l'assoce
				Adhesion.objects.create(eleve=utilisateur, association=assoce, role=fonction)
			return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/') # Redirect after POST
	else:
		form = AdhesionAjoutForm(assoce) # An unbound form

	return render_to_response('association/admin.html', {'form': form,},context_instance=RequestContext(request))
	
	
@login_required	
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
def changer_ordre(request, association_pseudo):
	assoce = get_object_or_404(Association,pseudo=association_pseudo)
	membres = Adhesion.objects.filter(association__pseudo = association_pseudo).order_by('-ordre', 'eleve__last_name')
	nombre_membres = Adhesion.objects.filter(association__pseudo = association_pseudo).count()
	if request.method == 'POST': # If the form has been submitted...
		if Adhesion.objects.filter(association=assoce, eleve=request.user).exists():#Si l'eleve est membre de l'assoce
			for i in range(1,nombre_membres+1):#Boucle sur les eleves
				adhesion = get_object_or_404(Adhesion,eleve__user__username=request.POST['login-'+str(i)], association = assoce)#On recupert l'eleve par son login
				adhesion.ordre = request.POST['position-'+str(i)]#On change sa position
				adhesion.save()
		return HttpResponseRedirect('/associations/'+assoce.pseudo+'/equipe/') # Redirect after POST
	return render_to_response('association/ordre.html', {'association':assoce, 'membres': membres, 'indices_membres': range(nombre_membres)},context_instance=RequestContext(request))