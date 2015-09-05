# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from faq.models import Question, Reponse, QuestionForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect


def accueil(request):
    return render_to_response('accueil/accueil.html', {},context_instance=RequestContext(request))

def admissibles(request):
    return render_to_response('admissibles/admissibles.html', {},context_instance=RequestContext(request))

def admis(request):
    return render_to_response('admis/admis.html', {},context_instance=RequestContext(request))

def logement(request):
    return render_to_response('admis/logement.html', {},context_instance=RequestContext(request))

def rentree(request):
    return render_to_response('admis/rentree.html', {},context_instance=RequestContext(request))

def questions(request):
    liste_questions = Question.objects.exclude(reponse = None).order_by('-date')

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
    
def poser_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        print "form cree"
        if form.is_valid():
            print "form valide"
            model = form.save()
            print "form saved " + str(model)
            try :
                 objet=form.cleaned_data['objet']
                 message=form.cleaned_data['contenu']
                 send_mail('Question posée sur la FAQ du portail',"Objet : " + objet + "\nMessage : "+ message, 'maxime.brunet@mines-paristech.fr',['maxime.brunet@mines-paristech.fr'], fail_silently=False)
            except BadHeaderError :
                 return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/faq/question_posee')
            # do something.
    else:
        form = QuestionForm()
    return render_to_response("faq/poser_question.html", {'form': form},context_instance=RequestContext(request))

def question_posee(request):
    return render_to_response('faq/question_posee.html', {},context_instance=RequestContext(request))