#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from pr.models import Clip
from django.template import RequestContext
from association.models import Association


@login_required
def lecteur(request):

	return render_to_response('radiopsl/lecteur.html', context_instance=RequestContext(request))