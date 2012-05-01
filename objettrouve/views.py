from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from objettrouve.models import ObjetTrouve, ObjetAjoutForm, ObjetSuppressionForm
from django.http import HttpResponseRedirect


# Create your views here.

@login_required
def index(request):
	liste_objets_trouves = ObjetTrouve.objects.filter(trouve=True).order_by('-date')
	liste_objets_perdus = ObjetTrouve.objects.filter(trouve=False).order_by('-date')
	return render_to_response('objettrouve/index.html', {'liste_objets_trouves': liste_objets_trouves,'liste_objets_perdus': liste_objets_perdus},context_instance=RequestContext(request))
	

@login_required	
def ajouter(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ObjetAjoutForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			elev = request.user.get_profile()
			desc = form.cleaned_data['description']
			trouv = form.cleaned_data['trouve']
			dat = form.cleaned_data['date']
			lie = form.cleaned_data['lieu']
			ObjetTrouve.objects.create(eleve=elev, trouve = trouv, description=desc, date=dat, lieu=lie)
			return HttpResponseRedirect('/objetstrouves/') # Redirect after POST
	else:
		form = ObjetAjoutForm() # An unbound form

	return render_to_response('objettrouve/form.html', {'form': form,},context_instance=RequestContext(request))
	
	
@login_required	
def supprimer(request):
	if request.method == 'POST': # If the form has been submitted...
		form = ObjetSuppressionForm(request.user, request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			objet = form.cleaned_data['objettrouve']
			if ObjetTrouve.objects.filter(id=objet.id, eleve=request.user).exists():
				ObjetTrouve.objects.filter(id=objet.id, eleve=request.user).delete()
			return HttpResponseRedirect('/objetstrouves/') # Redirect after POST
	else:
		form = ObjetSuppressionForm(request.user) # An unbound form

	return render_to_response('objettrouve/form.html', {'form': form,},context_instance=RequestContext(request))
	