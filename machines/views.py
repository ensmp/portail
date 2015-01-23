#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from trombi.tools import update_profile
from association.models import Adhesion
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.conf import settings
from urllib import urlretrieve
import subprocess
import vobject
import Image
import json
import os
from machines.models import MachineProfile

@csrf_exempt
def machines_update(request):
    """
        Mise à jour du statut des machines

        Cette page est appelée par le petit PC des machines.
        Le serveur envoie une requête POST sur cette page toutes les deux minutes
        pour mettre à jour les données des statuts.

    """
    json_machines = json.loads(request.POST.get('statut_machines', '[]'))
    for machine in json_machines:
        try:
            statutMachine = MachineProfile.objects.get(machine__nom = machine['nom'])
            statutMachine.etat = machine['etat']  
            statutMachine.save()
        except MachineProfile.DoesNotExist:                
            pass
    return HttpResponse('OK')