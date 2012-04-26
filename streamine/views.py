from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.template import RequestContext

def index(request):
	return render_to_response('streamine/index.html',context_instance=RequestContext(request))
