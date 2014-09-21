#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from bda.models import Revue
import json
from mineshake.models import UpdateSoldeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from django.contrib import messages


@permission_required('mineshake.change_soldesMineshake')
@login_required    
# Crediter le compte d'un élève
def soldes(request):
    if request.method == 'POST': 
        form = UpdateSoldeForm(request.POST) # formulaire associé aux données POST
        if form.is_valid(): # Formulaire valide
            utilisateur = form.cleaned_data['eleve']
            credit = form.cleaned_data['credit']
            debit = form.cleaned_data['debit']
            utilisateur.update_solde_mineshake(-credit)
            utilisateur.update_solde_mineshake(+debit)
            messages.add_message(request, messages.INFO, "Le compte a bien été modifié.")
            return redirect('mineshake.views.soldes')
    else:
        form = UpdateSoldeForm() # formulaire vierge
    return render_to_response('mineshake/soldes.html', {'form': form,},context_instance=RequestContext(request))