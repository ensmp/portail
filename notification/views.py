# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from notification.models import Envoi, Notification
from django.contrib.auth.decorators import login_required
from association.models import Association
from django.http import HttpResponseRedirect



@login_required
def liste(request):
	envoi_list = Envoi.objects.filter(user__username = request.user.username).order_by('-notification__date')
	envoi_list = envoi_list.exclude(notification__content_type__model = "Message") #On n'affiche pas les notifications de nouveaux messages
	envoi_nonlu_list = list(envoi_list.filter(lu = False))
	envoi_lu_list = list(envoi_list.filter(lu = True))
	mark_all_seen(request.user)
	return render_to_response('notification/liste.html',{'envoi_nonlu_list': envoi_nonlu_list, 'envoi_lu_list': envoi_lu_list},context_instance=RequestContext(request))

def mark_all_seen(user):
	notification_list = Notification.objects.filter(destinataires__username = user.username)
	for notification in notification_list:
		notification.lire(user)

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