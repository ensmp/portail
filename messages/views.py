#-*- coding: utf-8 -*-
from messages.models import Message
from trombi.models import UserProfile
from association.models import Association, Adhesion
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.template import RequestContext
from django.db.models import Q
from datetime import datetime


def index_json(request):
	message_list = Message.objects.order_by('-date')
	response = HttpResponse(mimetype='application/json')
	response.write(simplejson.dumps([{
			'association': m.association.nom,
			'objet': m.objet,
			'contenu': m.contenu,
			'date': str(m.date.day)+'/'+str(m.date.month)+'/'+str(m.date.year)+ " " + str(m.date.hour) + ":" + str(m.date.minute), 
			'expediteur': m.expediteur.user.username
		} for m in message_list]))
	return response

@login_required
def index(request):
	#list_messages = Message.objects.all()
	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all())).exclude(lu__user__username=request.user.username).order_by('-date')
	return render_to_response('messages/index.html', {'list_messages': list_messages},context_instance=RequestContext(request))
	
@login_required
def detail(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	#list_commentaires = Commentaire.objects.filter(message=m)
	return render_to_response('messages/detail.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
def lire(request, message_id):
	m = get_object_or_404(Message, pk=message_id)	
	m.lu.add(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
def classer_important(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.important.add(request.user.get_profile())
	m.lu.add(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
def classer_non_important(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.important.remove(request.user.get_profile())	
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
def classer_non_lu(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.lu.remove(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
def tous(request):

	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all())).order_by('-date')
	return render_to_response('messages/tous.html', {'list_messages': list_messages},context_instance=RequestContext(request))

@login_required
def importants(request):
	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all())).filter(important__user__username=request.user.username).order_by('-date')
	return render_to_response('messages/importants.html', {'list_messages': list_messages},context_instance=RequestContext(request))
	

@login_required
def nouveau(request, association_pseudo):
	if request.method == 'POST':
		if request.POST['dest'] == 'tous':
			receiver = None
		else:
			receiver = Association.objects.get(pseudo = request.POST['dest'])
		if Adhesion.objects.filter(association=get_object_or_404(Association,pseudo=association_pseudo), eleve=request.user).exists():
			Message.objects.create(association=Association.objects.get(pseudo=association_pseudo),objet=request.POST['title'],contenu=request.POST['body'],date=datetime.now(),expediteur=request.user.get_profile(), destinataire=receiver)
		return redirect('/associations/'+association_pseudo)
	else:
		liste_assoces = request.user.get_profile().association_set.all()
		return render_to_response('messages/nouveau.html', {'liste_assoces': liste_assoces},context_instance=RequestContext(request))