#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from trombi.models import UserProfile, Question, Reponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import Http404, HttpResponse
import json
import os

@login_required
def page2048(request):

	liste_eleves_score = UserProfile.objects.order_by("-meilleur_score_2048")[:10]
	print liste_eleves_score
 
	return render_to_response('2048/2048.html', {"liste_eleves_score": liste_eleves_score}, context_instance = RequestContext(request))


@login_required
def givescore(request):
	score = request.REQUEST.get("score")

	try:
		score = int(score)
	except:
		return HttpResponse("Not a number")

	if (not score or score > request.user.userprofile.meilleur_score_2048):
		request.user.userprofile.meilleur_score_2048 = score
		request.user.userprofile.save()
	return HttpResponse(score)