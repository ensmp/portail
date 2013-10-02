#-*- coding: utf-8 -*-
from entreprise.models import Entreprise,EvenementEntreprise
from trombi.models import UserProfile
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

def index(request):
    entreprises = Entreprise.objects.order_by('ordre');
    return render_to_response('entreprise/index.html', {'entreprises' : entreprises},context_instance=RequestContext(request))


def presentation_entreprises(request):
    return render_to_response('entreprise/presentation_entreprises.html', {}, context_instance=RequestContext(request))

def contact_entreprises(request):
    return render_to_response('entreprise/contact_entreprises.html', {}, context_instance=RequestContext(request))

def planning(request):
    evenement_entreprises = EvenementEntreprise.objects.order_by('-evenement');
    return render_to_response('entreprise/planning.html', {'evenement_entreprises':evenement_entreprises}, context_instance=RequestContext(request))