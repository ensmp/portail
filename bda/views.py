#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from bda.models import Revue
import json
from bda.models import UpdateSoldeFormBda
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile

@login_required
def archives(request):
    """
        La liste des Revues du BDA visibles par l'utilisateur
    """
    liste_revues = Revue.objects.all()
    return render_to_response('bda/revues.html', {'liste_revues': liste_revues}, context_instance=RequestContext(request))

@login_required
def archives_json(request):
    """
        Sérialisation au format JSON de la liste des Revues du BDA visibles par l'utilisateur
    """
    liste_revues = Revue.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_revues]))
    return response

@login_required
def musiciens(request):
    """
        La liste des musiciens du BDA visibles par l'utilisateur
    """
    
    return render_to_response('bda/musiciens.html', context_instance=RequestContext(request))

@login_required
#@permission_required('bda.add_liste')
def bda_update(request):
    """
        Mise à jour des soldes bda

    """
    json_octo = json.loads(request.POST.get('clients_bda', '[]'))
    for eleve in json_octo:
        try:
            profile = UserProfile.objects.get(user__username = eleve['login'])
            profile.solde_bda = eleve['solde_bda']   
            profile.save()
        except UserProfile.DoesNotExist:                
            pass
    return HttpResponse('OK')

@permission_required('bda.add_commande')
@login_required    
# Crediter le compte d'un élève
def credit_debit_eleve(request):
    if request.method == 'POST': 
        form = UpdateSoldeFormBda(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            credit = form.cleaned_data['credit']
            debit = form.cleaned_data['debit']
            utilisateur.update_solde_bda(-credit)
            utilisateur.update_solde_bda(+debit)
            messages.add_message(request, messages.INFO, "Le compte a bien été modifié.")
            return redirect('bda.views.credit_debit_eleve')
    else:
        form = UpdateSoldeFormBda() # formulaire vierge
    return render_to_response('bda/credit_debit_eleve.html', {'form': form,},context_instance=RequestContext(request))