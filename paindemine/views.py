# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from paindemine.models import Produit, Commande, Achat
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.db.models import Max
import json
from paindemine.models import UpdateSoldeForm
from django.contrib import messages

@login_required
def catalogue_pain(request):		
	liste_produits = Produit.objects.order_by('categorie', 'nom')
	return render_to_response('paindemine/catalogue_pain.html', {'liste_produits': liste_produits},context_instance=RequestContext(request))

@login_required
def commande(request):
	try:
		commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		liste_achats = Achat.objects.filter(commande__id = commande.id)
		total = 0
		for achat in liste_achats:
			nb_jour = achat.nb_jours()
			total = total + achat.produit.prix_vente*achat.quantite*nb_jour	
	except Commande.DoesNotExist:
		liste_achats = None	
		total = 0
	return render_to_response('paindemine/commande.html', {'liste_achats': liste_achats,'total':total},context_instance=RequestContext(request))

@login_required
def acheter(request):
	if request.POST:
		try:
			commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False)
		except Commande.DoesNotExist:
			commande = Commande.objects.create(eleve = request.user.get_profile())
		produit = get_object_or_404(Produit, id = request.POST['id'])
		if request.POST['quantite'] != "0":
			lundi = 0
			mercredi = 0
			jeudi = 0
			for jour in request.POST.getlist('jour'):
				if 'lundi'== jour:
					lundi=1
				if 'mercredi'== jour:
					mercredi=1
				if 'jeudi'== jour:
					jeudi=1
			achat = Achat.objects.create(commande = commande, produit = produit, quantite = request.POST['quantite'], lundi = lundi, mercredi = mercredi, jeudi = jeudi)		
		return redirect('paindemine.views.commande')

@login_required
def commander(request):
	commande = Commande.objects.get(eleve__user__username=request.user.username, fermee=False) #On recupere la commande dont l'eleve est l'utilisateur qui request la page, qui doit être encore ouverte
	commande.fermee = True #On la ferme
	commande.date_fermeture = datetime.today() #On enregistre la date de fermeture
	commande.save() #On enregistre
	return redirect('paindemine.views.catalogue_pain')

@login_required
def fermer_commandes(request):
	Commande.objects.filter(fermee = False).update(fermee = True, date_fermeture = datetime.today())
	return redirect('paindemine.views.catalogue_pain')
	
@login_required
def dernieres_commandes(request):	
	liste_commandes = Commande.objects.filter(date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max'])
	return liste_commandes
	
def dernieres_commandes_csv(request):
	from django.template import loader, Context
	liste_commandes = dernieres_commandes(request)
	date_fermeture = Commande.objects.aggregate(Max('date_fermeture'))['date_fermeture__max']
	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=dernieres_commandes.csv'
	t = loader.get_template('paindemine/dernieres_commandes.txt')
	c = Context({'liste_commandes': liste_commandes,'date_fermeture':date_fermeture})
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
	return redirect('paindemine.views.commande')
	
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
	return redirect('paindemine.views.commande')

@permission_required('paindemine.change_soldespaindemine')
@login_required    
# Crediter le compte d'un élève
def soldespaindemine(request):
    if request.method == 'POST': 
        form = UpdateSoldeForm(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            credit = form.cleaned_data['credit']
            debit = form.cleaned_data['debit']
            utilisateur.update_solde_paindemine(-credit)
            utilisateur.update_solde_paindemine(+debit)
            messages.add_message(request, messages.INFO, "Le compte a bien été modifié.")
            return redirect('paindemine.views.soldespaindemine')
    else:
        form = UpdateSoldeForm() # formulaire vierge
    return render_to_response('paindemine/soldes.html', {'form': form,},context_instance=RequestContext(request))

@permission_required('paindemine.change_soldespaindemine')
@login_required    
# Crediter le compte d'un élève
def affichagesoldes(request):

    mineur_list = UserProfile.objects.promos_actuelles(3)
    liste_eleves = []
    for eleve in mineur_list :
    	if eleve.solde_paindemine != 0:
    		liste_eleves.append((u'{0} {1}'.format(eleve.first_name, eleve.last_name),eleve.solde_paindemine))

    return render_to_response('paindemine/affichagesoldes.html', {'liste_eleve' : liste_eleves},context_instance=RequestContext(request))