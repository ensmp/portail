# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from freshbox.models import Commande, UpdateSoldeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Max
from django.contrib import messages

@login_required
def catalogueFresh(request):		
	return render_to_response('freshbox/catalogueFresh.html', {},context_instance=RequestContext(request))


@login_required
def commande(request):
	try:
		solde = request.user.get_profile().solde_freshbox
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
	except Commande.DoesNotExist:
		commande = None
	return render_to_response('freshbox/commande.html', {'commande':commande, 'solde_freshbox':solde},context_instance=RequestContext(request))

@login_required
def acheter(request):
	if request.POST:
		try:
			commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		except Commande.DoesNotExist:
			commande = Commande.objects.create(eleve = request.user.get_profile())
	return redirect('freshbox.views.commande')

@login_required
def commander(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False) #On recupere la commande dont l'eleve est l'utilisateur qui request la page, qui doit être encore ouverte
	commande.fermee = True #On la ferme
	commande.date_fermeture = datetime.today() #On enregistre la date de fermeture
	commande.save() #On enregistre
	return redirect('freshbox.views.catalogueFresh')

@login_required
def fermer_commandes(request):
	Commande.objects.filter(fermee = False).update(fermee = True, date_fermeture = datetime.today())
	return redirect('freshbox.views.catalogueFresh')
	
@login_required
def dernieres_commandes(request):	
	liste_commandes = Commande.objects.filter(date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max'])
	return liste_commandes
	
def dernieres_commandes_csv(request):
	from django.template import loader, Context
	liste_commandes = dernieres_commandes(request)
	date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max']
	response = HttpResponse(mimetype='text/csv; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=dernieres_commandes.csv'

	t = loader.get_template('freshbox/dernieres_commandes.txt')
	c = Context({'liste_commandes': liste_commandes, 'date_fermeture': date_fermeture})
	response.write(t.render(c))
	return response
	

@login_required
def valider_commande(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
	if float(10.0) > request.user.get_profile().solde_freshbox:
		messages.add_message(request, messages.ERROR, "Pas assez d'argent sur votre compte de Freshbox.")
	else:
		request.user.get_profile().update_solde_freshbox(10.0)
		commande.validee = True
		commande.save()
		messages.add_message(request, messages.INFO, "Commande validée.")
	return redirect('freshbox.views.commande')

@login_required
def supprimer_commande(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
	commande.delete()	
	return redirect('freshbox.views.commande')


@permission_required('freshbox.add_produit')
@login_required    
# Crediter le compte d'un élève
def credit_eleve(request):
    if request.method == 'POST': 
        form = UpdateSoldeForm(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            prix = form.cleaned_data['credit']
            utilisateur.update_solde_freshbox(-prix)
            messages.add_message(request, messages.INFO, "Le compte a bien été crédité.")
            return redirect('freshbox.views.credit_eleve')
    else:
        form = UpdateSoldeForm() # formulaire vierge
    return render_to_response('freshbox/credit_eleve.html', {'form': form,},context_instance=RequestContext(request))

@login_required
def export_soldes(request):	
	liste_eleves = UserProfile.objects.exclude(solde_freshbox = 0)
	return liste_eleves
	
def export_soldes_csv(request):
	from django.template import loader, Context
	liste_eleves = export_soldes(request)
	response = HttpResponse(mimetype='text/csv; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=export_soldes.csv'
	t = loader.get_template('freshbox/export_soldes.txt')
	c = Context({'liste_eleves': liste_eleves})
	response.write(t.render(c))
	return response