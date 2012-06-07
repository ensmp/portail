from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from vendome.models import UploadFileForm, Vendome
from django.core.context_processors import csrf
  

def index(request):
    if request.method == 'POST':
        a=request.POST
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['fichier'])
            nouveauvendome = Vendome.objects.create(titre=request.POST['titre'], fichier = request.FILES['fichier'].name.replace(" ", "_"), date = request.POST['date'])
            nouveauvendome.save()
            return HttpResponseRedirect('/associations/vendome/page/')
    else:
        form = UploadFileForm()

    c = {'form': form}
    c.update(csrf(request))
    return render_to_response('vendome/nouveau.html', c)

def handle_uploaded_file(file):
#    logging.debug("upload_here")
    if file:
        destination = open(settings.STATIC_ROOT +'docs/'+file.name.replace(" ", "_"), 'wb+')
        #destination = open('/tmp/'+file.name, 'wb+')
        #destination = open('/tmp', 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
		

def page(request):
    liste_vendomes = Vendome.objects.all().order_by('-date')
    return render_to_response('vendome/page.html', {'liste_vendomes': liste_vendomes},context_instance=RequestContext(request))