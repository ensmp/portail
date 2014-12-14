#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from pr.models import Clip
from django.template import RequestContext
from association.models import Association


@login_required
def clips(request):

	pr = Association.objects.filter(id=30)[0]
	if request.user.get_profile().en_premiere_annee() and pr.is_hidden_1A == True:
		clip_list = []
	else :
		clip_list = Clip.objects.all()
		
	return render_to_response('pr/clips.html', {'clip_list': clip_list}, context_instance=RequestContext(request))