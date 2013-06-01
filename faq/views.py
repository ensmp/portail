#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from faq.models import Question, Reponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def accueil(request):
	return render_to_response('accueil/accueil.html', {},context_instance=RequestContext(request))

def questions(request):
	liste_questions = Question.objects.exclude(reponse = None)

	paginator = Paginator(liste_questions, 10) # 10 questions par page
	
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		# Si la page n'est pas un entier, afficher la premiere page.
		questions = paginator.page(1)
	except EmptyPage:
		# Si la page est incorrecte (e.g. 9999), afficher la derniere page.
		questions = paginator.page(paginator.num_pages)
		
	return render_to_response('faq/questions.html', {'questions': questions},context_instance=RequestContext(request))