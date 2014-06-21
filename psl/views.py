#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from psl.models import newsletter
import json

@login_required
def archives(request):
    """
        La liste des newsletters de PSL visibles par l'utilisateur
    """
    liste_newsletters = newsletter.objects.all()
    return render_to_response('psl/newsletter.html', {'liste_newsletters': liste_newsletters}, context_instance=RequestContext(request))

@login_required
def archives_json(request):
    """
        Sérialisation au format JSON de la liste des newsletters de PSL visibles par l'utilisateur
    """
    liste_newsletters = newsletter.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_newsletters]))
    return response
