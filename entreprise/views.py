#-*- coding: utf-8 -*-
from entreprise.models import Entreprise
from trombi.models import UserProfile
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q

def index(request):
    entreprises = Entreprise.objects.order_by('ordre');
    return render_to_response('entreprise/index.html', {'entreprises' : entreprises},context_instance=RequestContext(request))