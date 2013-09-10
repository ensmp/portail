#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from vendome.models import Vendome
import json

@login_required
def archives(request):
    """
        La liste des Vendômes visibles par l'utilisateur
    """
    liste_vendomes = Vendome.objects.all()
    if request.user.get_profile().en_premiere_annee():
        liste_vendomes = liste_vendomes.exclude(is_hidden_1A = True)
    return render_to_response('vendome/archives.html', {'liste_vendomes': liste_vendomes}, context_instance=RequestContext(request))

@login_required
def archives_json(request):
    """
        Sérialisation au format JSON de la liste des vendômes visibles par l'utilisateur
    """
    liste_vendomes = Vendome.objects.all()
    if request.user.get_profile().en_premiere_annee() or request.user.get_profile().ast_en_deuxieme_annee():
        liste_vendomes = liste_vendomes.exclude(is_hidden_1A = True)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_vendomes]))
    return response
