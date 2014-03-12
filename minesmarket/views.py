# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from minesmarket.models import Produit, Commande, Achat, UpdateSoldeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Max
from django.contrib import messages

@login_required
def catalogue(request):		
	liste_produits = Produit.objects.order_by('categorie', 'nom').filter(metro=False)
	return render_to_response('minesmarket/catalogue.html', {'liste_produits': liste_produits},context_instance=RequestContext(request))

@login_required
def catalogue_metro(request):		
	liste_produits = Produit.objects.order_by('categorie', 'nom').filter(metro=True)
	return render_to_response('minesmarket/catalogue_metro.html', {'liste_produits': liste_produits},context_instance=RequestContext(request))


@login_required
def commande(request):
	try:
		solde = request.user.get_profile().solde_minesmarket
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id = commande.id)
		total = commande.total()
	except Commande.DoesNotExist:
		commande = None
		liste_achats = None	
		total = 0
	return render_to_response('minesmarket/commande.html', {'commande':commande, 'liste_achats': liste_achats, 'total' : total, 'solde_minesmarket':solde},context_instance=RequestContext(request))

@login_required
def acheter(request):
	if request.POST:
		try:
			commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		except Commande.DoesNotExist:
			commande = Commande.objects.create(eleve = request.user.get_profile())
		
		if not commande.validee:
			produit = get_object_or_404(Produit, id = request.POST['id'])
			try:
				achat = Achat.objects.get(commande__id = commande.id, produit__id = produit.id)
				if request.POST['quantite'] == "0":
					achat.delete()
				else:
					achat.quantite = request.POST['quantite']
					achat.save()
			except Achat.DoesNotExist:
				if request.POST['quantite'] != "0":
					achat = Achat.objects.create(commande = commande, produit = produit, quantite = request.POST['quantite'])
		else:
			messages.add_message(request.POST, messages.ERROR, "Erreur : commande déjà validée")	
	return redirect('minesmarket.views.commande')

@login_required
def commander(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False) #On recupere la commande dont l'eleve est l'utilisateur qui request la page, qui doit être encore ouverte
	commande.fermee = True #On la ferme
	commande.date_fermeture = datetime.today() #On enregistre la date de fermeture
	commande.save() #On enregistre
	return redirect('minesmarket.views.catalogue')

@login_required
def fermer_commandes(request):
	Commande.objects.filter(fermee = False).update(fermee = True, date_fermeture = datetime.today())
	return redirect('minesmarket.views.catalogue')
	
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

	t = loader.get_template('minesmarket/dernieres_commandes.txt')
	c = Context({'liste_commandes': liste_commandes, 'date_fermeture': date_fermeture})
	response.write(t.render(c))
	return response
	
@login_required
def supprimer_achat(request, id_achat):
	achat = get_object_or_404(Achat, id = id_achat)
	print "achat" + str(achat)
	commande = achat.commande
	if achat.commande.eleve.user == request.user and achat.commande.fermee == False:
		achat.delete()
	print "commande" + str(commande)
	return redirect('minesmarket.views.commande')
	
@login_required
def supprimer_tous_achats(request):
	try:
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id = commande.id)
		total = 0
		for achat in liste_achats:
			achat.delete()	
	except Commande.DoesNotExist:
		liste_achats = None	
		total = 0
	return redirect('minesmarket.views.commande')

@login_required
def valider_commande(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
	if float(commande.total()) > request.user.get_profile().solde_minesmarket:
		messages.add_message(request, messages.ERROR, "Pas assez d'argent sur votre compte de MinesMarket.")
	else:
		request.user.get_profile().update_solde_minesmarket(commande.total())
		commande.validee = True
		commande.save()
		messages.add_message(request, messages.INFO, "Commande validée.")
	return redirect('minesmarket.views.commande')

@permission_required('minesmarket.add_produit')
@login_required    
# Crediter le compte d'un élève
def credit_eleve(request):
    if request.method == 'POST': 
        form = UpdateSoldeForm(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            prix = form.cleaned_data['credit']
            utilisateur.update_solde_minesmarket(-prix)
            messages.add_message(request, messages.INFO, "Le compte a bien été crédité.")
            return redirect('minesmarket.views.credit_eleve')
    else:
        form = UpdateSoldeForm() # formulaire vierge
    return render_to_response('minesmarket/credit_eleve.html', {'form': form,},context_instance=RequestContext(request))

@login_required
def export_soldes(request):	
	liste_eleves = UserProfile.objects.exclude(solde_minesmarket = 0)
	return liste_eleves
	
def export_soldes_csv(request):
	from django.template import loader, Context
	liste_eleves = export_soldes(request)
	response = HttpResponse(mimetype='text/csv; charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename=export_soldes.csv'
	t = loader.get_template('minesmarket/export_soldes.txt')
	c = Context({'liste_eleves': liste_eleves})
	response.write(t.render(c))
	return response