# -*- coding: utf-8 -*-
from mediamines.models import Photo
from trombi.models import UserProfile
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
import json



@login_required
#Identifier un eleve a une photo
def identifier(request, slug):
	response = HttpResponse()		
	if request.POST:
		photo = get_object_or_404(Photo, title_slug = slug)
		eleve = get_object_or_404(UserProfile, user__username = request.POST['username'])
		photo.eleves.add(eleve)
		response.write('post ' + slug)
	return response

@login_required
#Desidentifier un eleve d'une photo
def desidentifier(request, slug):
	response = HttpResponse()		
	if request.POST:
		photo = get_object_or_404(Photo, title_slug = slug)
		if request.POST.get('username'):
			eleve = get_object_or_404(UserProfile, user__username = request.POST['username'])
			photo.eleves.remove(eleve)
		else:
			photo.eleves.clear()
		response.write('post ' + slug)
	return response

@login_required
#La liste (format JSON) des eleves identifies sur une photo
def identifications(request, slug):
	response = HttpResponse()		
	photo = get_object_or_404(Photo, title_slug = slug)
	response.write(json.dumps([{
		'username': e.user.username			
	} for e in photo.eleves.all()]))
	return response