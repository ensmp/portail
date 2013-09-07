from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from palum.models import UploadFileForm, Palum
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required

  

@login_required
@permission_required('palum.add_palum')
def nouveau(request):
    if request.method == 'POST':
        a=request.POST
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            nouveaupalum = Palum.objects.create(annee = request.FILES['annee'] ,fichier = request.FILES['fichier'], date = request.POST['date'])
            nouveaupalum.save()
            return HttpResponseRedirect('palum/nouveau.html')
    else:
        form = UploadFileForm()
    return render_to_response('palum/nouveau.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def archives(request):
    liste_palums = Palum.objects.order_by('-date')
    liste_palums_1A = liste_palums.filter(annee=1)
    liste_palums_2A = liste_palums.filter(annee=2)
    liste_palums_3A = liste_palums.filter(annee=3)
    return render_to_response('palum/archives.html', {'liste_palums_1A': liste_palums_1A,'liste_palums_2A': liste_palums_2A,'liste_palums_3A': liste_palums_3A},context_instance=RequestContext(request))

@login_required
def archives_json(request):
    liste_palums = Palum.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'annee': p.annee,
            'fichier': p.fichier.url,
            'date': p.date
        } for p in liste_palums]))
    return response
