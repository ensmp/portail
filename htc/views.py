#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from htc.models import Revue
import json
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from django.contrib import messages

@login_required
def newsletter(request):
    """
        La liste des Revues du htc visibles par l'utilisateur
    """
    liste_newsletter = Revue.objects.all()
    return render_to_response('htc/newsletter.html', {'liste_newsletter': liste_newsletter}, context_instance=RequestContext(request))

@login_required
def archives_json(request):
    """
        Sérialisation au format JSON de la liste des Revues du htc visibles par l'utilisateur
    """
    liste_newsletter = Revue.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_revues]))
    return response

