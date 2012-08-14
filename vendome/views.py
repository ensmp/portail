from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from vendome.models import UploadFileForm, Vendome
from django.core.context_processors import csrf
  

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

def archives(request):
    liste_vendomes = Vendome.objects.all().order_by('-date')
    return render_to_response('vendome/archives.html', {'liste_vendomes': liste_vendomes},context_instance=RequestContext(request))