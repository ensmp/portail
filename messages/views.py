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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
#La liste des nouveaux messages
def index(request):
	#On sélectionne les messages publics, et les messages dont l'utilisateur fait partie de l'assoce expeditrice, ou de l'assoce destinataires.
	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all()) | Q(association__in=request.user.get_profile().association_set.all())).exclude(lu__user__username=request.user.username).order_by('-date')
	return render_to_response('messages/index.html', {'list_messages': list_messages},context_instance=RequestContext(request))

@login_required
#La liste des nouveaux messages, sérialisée aux format JSON (pour les applis)
def index_json(request):
	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all()) | Q(association__in=request.user.get_profile().association_set.all())).exclude(lu__user__username=request.user.username).order_by('-date')
	response = HttpResponse(mimetype='application/json')
	response.write(simplejson.dumps([{
			'association': m.association.nom,
			'association_pseudo': m.association.pseudo,
			'objet': m.objet,
			'contenu': m.contenu,
			'date': str(m.date.day)+'/'+str(m.date.month)+'/'+str(m.date.year)+ " " + str(m.date.hour) + ":" + str(m.date.minute), 
			'expediteur': m.expediteur.user.username			
		} for m in list_messages]))
	return response
	
@login_required
#L'affichage des détails d'un message (de ses commentaires)
def detail(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	return render_to_response('messages/detail.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
#Permet de classer un message comme lu (UNSAFE via un GET --> A changer en POST)
def lire(request, message_id):
	m = get_object_or_404(Message, pk=message_id)	
	m.lu.add(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
#Permet de classer un message comme important (UNSAFE via un GET --> A changer en POST)
def classer_important(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.important.add(request.user.get_profile())
	m.lu.add(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))

@login_required	
#Permet de classer un message comme non important (UNSAFE via un GET --> A changer en POST)
def classer_non_important(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.important.remove(request.user.get_profile())	
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))

@login_required
#Permet de classer un message comme non lu (UNSAFE via un GET --> A changer en POST)
def classer_non_lu(request, message_id):
	m = get_object_or_404(Message, pk=message_id)
	m.lu.remove(request.user.get_profile())
	m.save()
	
	return render_to_response('messages/action.html', {'message': m},context_instance=RequestContext(request))
	
@login_required
#La liste des messages, y compris les messages lus (à paginer)
def tous(request):
	all_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all()) | Q(association__in=request.user.get_profile().association_set.all())).order_by('-date')
	
	paginator = Paginator(all_messages, 25)
	page = request.GET.get('page')
	try:
		list_messages = paginator.page(page)
	except PageNotAnInteger:        
		list_messages = paginator.page(1)
	except EmptyPage:        
		list_messages = paginator.page(paginator.num_pages)
	
	return render_to_response('messages/tous.html', {'list_messages': list_messages},context_instance=RequestContext(request))

@login_required
#La liste des messages classés importants
def importants(request):
	list_messages = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=request.user.get_profile().association_set.all()) | Q(association__in=request.user.get_profile().association_set.all())).filter(important__user__username=request.user.username).order_by('-date')
	return render_to_response('messages/importants.html', {'list_messages': list_messages},context_instance=RequestContext(request))
	

@login_required
#La création d'un nouveau message par une association
def nouveau(request, association_pseudo):
	if request.method == 'POST':
		if request.POST['dest'] == 'tous':
			receiver = None
		else:
			receiver = Association.objects.get(pseudo = request.POST['dest'])
		if Adhesion.objects.filter(association=get_object_or_404(Association,pseudo=association_pseudo), eleve=request.user).exists(): #Si l'utilisateur est membre de l'assoce
			Message.objects.create(association=Association.objects.get(pseudo=association_pseudo),objet=request.POST['title'],contenu=request.POST['body'],date=datetime.now(),expediteur=request.user.get_profile(), destinataire=receiver)
		return redirect('/associations/'+association_pseudo)
	else:
		liste_assoces = Association.objects.all()
		return render_to_response('messages/nouveau.html', {'liste_assoces': liste_assoces},context_instance=RequestContext(request))