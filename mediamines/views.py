from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from mediamines.models import Album

@login_required
def albums(request):
	liste_albums = Album.objects.all()
	return render_to_response('mediamines/albums.html', {'liste_albums':liste_albums},context_instance=RequestContext(request))
	
def detail(request, album_id):
	album = get_object_or_404(Album, pk=album_id)
	
	import os
	#albumspath = os.path.join("public", "media", "img", "mediamines", album.dossier)
	#os.chdir(albumspath)
	file_list = os.listdir("public/media/img/mediamines/"+album.dossier)
	return render_to_response('mediamines/detail.html', {'album':album, 'file_list':file_list},context_instance=RequestContext(request))