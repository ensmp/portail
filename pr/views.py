#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from pr.models import Clip
from django.template import RequestContext
from association.models import Association
from trombi.models import UserProfile
from pr.models import Candidat, Vote
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import json
from datetime import date, datetime, timedelta

import datetime

@login_required
def clips(request):

	pr = Association.objects.filter(id=30)[0]
	if request.user.get_profile().en_premiere_annee() and pr.is_hidden_1A == True:
		clip_list = []
	else :
		clip_list = Clip.objects.all()
		
	return render_to_response('pr/clips.html', {'clip_list': clip_list}, context_instance=RequestContext(request))


@login_required
def voter(request):
    debut_vote = None
    fin_vote = None
    peut_voter = False
    deja_vote = False

    if Candidat.objects.filter(debut_vote__gte = datetime.datetime.now()).count() > 0: #Une election va commencer
        debut_vote = (Candidat.objects.filter(debut_vote__gte = datetime.datetime.now())[0]).debut_vote

    listes = Candidat.objects.filter(debut_vote__lte = datetime.datetime.now(), fin_vote__gte = datetime.datetime.now())

    if listes.count() >= 1: #On peut voter
        peut_voter = True
        fin_vote = (Candidat.objects.all()[0]).fin_vote        
        if Vote.objects.filter(eleve = request.user.get_profile()).count()>1: #L'élève a déjà voté
            # messages.add_message(request, messages.ERROR, "Vous avez déjà voté !")
            peut_voter = False
            deja_vote = True
        elif Vote.objects.filter(eleve = request.user.get_profile()).count()==1:
            candidatDejaVote = Vote.objects.get(eleve = request.user.get_profile()).liste.id
            listes= listes.exclude(id=candidatDejaVote)


    if listes.count()>0 :
        if request.POST :
            name = request.POST['choix']

            if Candidat.objects.filter(nom = name).exists() :
                if Vote.objects.filter(eleve = request.user.get_profile()).count()==1:
                    liste = get_object_or_404(Candidat, nom = name)
                    if Vote.objects.filter(eleve = request.user.get_profile(),liste__nom = liste).exists() :
                        messages.add_message(request, messages.INFO, "Vous avez deja voté pour ce candidat !")
                    else :
                        liste.nbVotes = liste.nbVotes+1
                        liste.save()
                        Vote.objects.create(liste = liste, eleve=request.user.get_profile())
                        messages.add_message(request, messages.INFO, "A voté une seconde fois !")
                        peut_voter = False
                        deja_vote = True     


                if not deja_vote and Vote.objects.filter(eleve = request.user.get_profile()).count()!=1:
                    liste = get_object_or_404(Candidat, nom = name) 
                    liste.nbVotes = liste.nbVotes+1
                    liste.save()
                    Vote.objects.create(liste = liste, eleve=request.user.get_profile())
                    messages.add_message(request, messages.INFO, "A voté !")
                    peut_voter = False
                    deja_vote = True     

            if Vote.objects.filter(eleve = request.user.get_profile()).count()==1:
                peut_voter=True
                candidatDejaVote = Vote.objects.get(eleve = request.user.get_profile()).liste.id
                listes= listes.exclude(id=candidatDejaVote)

    if request.user.get_profile().promo != 12 and request.user.get_profile().promo != 13 :
    	peut_voter = False

    return render_to_response('pr/voter.html', {'peut_voter':peut_voter, 'deja_vote':deja_vote, 'listes':listes, 'debut_vote':debut_vote, 'fin_vote':fin_vote}, context_instance=RequestContext(request))
    
@login_required
@permission_required('pr.add_liste')
def resultats(request):
    listes = Candidat.objects.filter(debut_vote__lte = datetime.datetime.now())
    return render_to_response('pr/resultats.html', {'listes':listes}, context_instance=RequestContext(request))

@login_required
@permission_required('pr.add_liste')
def voir_votes(request):   
    liste_votes = Vote.objects.all()
    return liste_votes
    
def voir_votes_csv(request):
    from django.template import loader, Context
    liste_votes = voir_votes(request)
    response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=voir_votes.csv'

    t = loader.get_template('pr/voir_votes.txt')
    c = Context({'liste_votes': liste_votes})
    response.write(t.render(c))
    return response