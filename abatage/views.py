from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from abatage.models import Abatage
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def archives(request):
    liste_abatages = Abatage.objects.all()
    return render_to_response('abatage/archives.html', {'liste_abatages': liste_abatages},context_instance=RequestContext(request))

@login_required
def archives_json(request):
    liste_abatages = Abatage.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_abatages]))
    return response

def archives_visiteur(request):
    abatage_annuel = Abatage.objects.all()[0]
    liste_abatages = Abatage.objects.exclude(id = abatage_annuel.id)
    return render_to_response('abatage/archives_visiteur.html', {'abatage_annuel':abatage_annuel},context_instance=RequestContext(request))