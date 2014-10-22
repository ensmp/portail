# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from notification.models import Envoi, Notification
from django.contrib.auth.decorators import login_required
from association.models import Association
from django.http import HttpResponseRedirect



@login_required
def liste(request):
	envoi_list = Envoi.objects.filter(user = request.user).order_by('-notification__date')
	envois_non_lus = envoi_list.filter(lu = False)
	envois_lus = envoi_list.filter(lu = True)[:50]
	mark_all_seen(request.user)
	return render_to_response('notification/liste.html',{'envois_non_lus': envois_non_lus, 'envois_lus': envois_lus},context_instance=RequestContext(request))

def mark_all_seen(user):
	Envoi.objects.filter(user = user).update(lu = True)

@login_required
#Choisir les associations qu'on suit
def preferences(request):
	associations = Association.objects.all()
	if request.method == 'POST':
		request.user.associations_suivies.clear()
		for pseudo_assoce in request.POST:
			try:
				assoce = Association.objects.get(pseudo = pseudo_assoce)
				assoce.suivi_par.add(request.user)
				assoce.save()
			except Association.DoesNotExist:
				pass

		return HttpResponseRedirect('/notifications/')
	return render_to_response('notification/preferences.html', {'associations':associations},context_instance=RequestContext(request))