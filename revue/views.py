#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from revue.models import Revue
import json

@login_required
def archives(request):
    """
        La liste des Revues du BDA visibles par l'utilisateur
    """
    liste_revues = Revue.objects.all()
    return render_to_response('revue/archives.html', {'liste_revues': liste_revues}, context_instance=RequestContext(request))

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
