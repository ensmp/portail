# -*- coding: utf-8 -*-
from jump.models import Etude
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext


@login_required
#La liste des études JuMP
def etudes(request):
	liste_etudes = Etude.objects.all().order_by('date')
	return render_to_response('jump/etudes.html',{'liste_etudes': liste_etudes},context_instance=RequestContext(request))