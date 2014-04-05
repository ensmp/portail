#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from bilanmandat.models import QuestionBilan, VoteBilan
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required

import json
import datetime


@login_required
# Vote a un sondage
def voter(request):
    if QuestionBilan.objects.filter(vu = True).exists(): #Le sondage du jour a déjà été choisi
        #sondage = get_object_or_404(QuestionBilan, vu = True) #On le récupère
        sondage = QuestionBilan.objects.filter(vu = True)[0]
        if VoteBilan.objects.filter(questionBilan = sondage, eleve__user__username=request.user.username).exists(): #L'élève a déjà voté
            messages.add_message(request, messages.ERROR, "Vous avez déjà voté pour ce sondage")
        else:             
            if request.method == 'POST':
                if VoteBilan.objects.filter(questionBilan = sondage, reponse=int(request.POST['reponse'])).exists():
                    messages.add_message(request, messages.ERROR, "Quelqu'un a déjà donné cette réponse")
                else:
                    VoteBilan.objects.create(questionBilan = sondage, eleve=request.user.get_profile(), reponse = int(request.POST['reponse']))
                    messages.add_message(request, messages.INFO, "A voté !")
        return render_to_response('bilanmandat/voter.html', {'question':sondage},context_instance=RequestContext(request))
    else :
        return render_to_response('bilanmandat/voter.html', {},context_instance=RequestContext(request))


@permission_required('bilanmandat.add_questionbilan')
def results(request):
    questions = QuestionBilan.objects.filter(vu=True)
    if questions.exists(): #Le sondage du jour a déjà été choisi
        sondage = QuestionBilan.objects.filter(vu = True)[0]
        votes = VoteBilan.objects.filter(questionBilan=sondage).order_by('reponse')
        if (sondage.trouve()):
            vainqueur = VoteBilan.objects.filter(questionBilan=sondage, reponse = sondage.resultat)[0].eleve
            return render_to_response('bilanmandat/results.html', {'question':sondage, 'votes':votes, 'vainqueur':vainqueur},context_instance=RequestContext(request))
        else:
            return render_to_response('bilanmandat/results.html', {'question':sondage, 'votes':votes},context_instance=RequestContext(request))
    else:
        return render_to_response('bilanmandat/voter.html', {},context_instance=RequestContext(request))
    
    
@permission_required('bilanmandat.add_questionbilan')
def proche(request):
    questions = QuestionBilan.objects.filter(vu=True)
    if questions.exists(): #Le sondage du jour a déjà été choisi
        sondage = QuestionBilan.objects.filter(vu = True)[0]
        votes = VoteBilan.objects.filter(questionBilan=sondage)
        if votes.exists():
            n = abs(votes[0].reponse- sondage.resultat)
            vainqueur= votes[0].eleve
            for i in range(0,votes.count()):
                if (abs(votes[i].reponse- sondage.resultat)<n):
                    n = abs(votes[i].reponse- sondage.resultat)
                    vainqueur = votes[i].eleve
            return render_to_response('bilanmandat/proche.html', {'question':sondage,'vainqueur':vainqueur},context_instance=RequestContext(request))
        else:
            return voter(request)   
    else:
        return render_to_response('bilanmandat/voter.html', {},context_instance=RequestContext(request))