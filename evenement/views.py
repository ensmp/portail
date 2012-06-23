from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from evenement.models import Evenement

@login_required
def index(request):
	liste_evenements = Evenement.objects.all().order_by('date_debut')
	return render_to_response('evenement/calendrier.html', {'liste_evenements':liste_evenements},context_instance=RequestContext(request))