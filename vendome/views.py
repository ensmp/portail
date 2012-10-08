from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from vendome.models import UploadFileForm, Vendome
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required, permission_required

  

@login_required
@permission_required('vendome.add_vendome')
def nouveau(request):
    if request.method == 'POST':
        a=request.POST
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            nouveauvendome = Vendome.objects.create(titre=request.POST['titre'], fichier = request.FILES['fichier'], date = request.POST['date'])
            nouveauvendome.save()
            return HttpResponseRedirect('/associations/vendome/archives/')
    else:
        form = UploadFileForm()
    return render_to_response('vendome/nouveau.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def archives(request):
    liste_vendomes = Vendome.objects.all()
    if request.user.get_profile().en_premiere_annee():
        liste_vendomes = liste_vendomes.exclude(is_hidden_1A = True)
    return render_to_response('vendome/archives.html', {'liste_vendomes': liste_vendomes},context_instance=RequestContext(request))

@login_required
def archives_json(request):
    liste_vendomes = Vendome.objects.all()
    if request.user.get_profile().en_premiere_annee():
        liste_vendomes = liste_vendomes.exclude(is_hidden_1A = True)
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'titre': v.titre,
            'fichier': v.fichier.url,
            'date': str(v.date)
        } for v in liste_vendomes]))
    return response
