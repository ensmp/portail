from django.shortcuts import render_to_response, get_object_or_404
from pr.models import Clip
from django.template import RequestContext


def clips(request):
	clip_list = Clip.objects.all()
	return render_to_response('pr/clips.html', {'clip_list': clip_list}, context_instance=RequestContext(request))