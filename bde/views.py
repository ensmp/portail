#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from bde.models import Liste, Vote, Palum, ParrainageVoeux, ParrainageVoeuxForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
import json
from datetime import date, datetime, timedelta

import datetime

@login_required
# Vote pour une liste
def voter(request):
    debut_vote = None
    fin_vote = None
    peut_voter = False
    deja_vote = False
    liste1 = None
    liste2 = None
    if Liste.objects.filter(debut_vote__gte = datetime.datetime.now()).count() > 0: #Une election va commencer
        debut_vote = (Liste.objects.filter(debut_vote__gte = datetime.datetime.now())[0]).debut_vote
    
    listes = Liste.objects.filter(debut_vote__lte = datetime.datetime.now(), fin_vote__gte = datetime.datetime.now())
    if listes.count() >= 2: #On peut voter
        peut_voter = True
        fin_vote = (Liste.objects.all()[0]).fin_vote
        liste1 = listes[0]
        liste2 = listes[1]        
        if Vote.objects.filter(eleve = request.user.get_profile()).exists(): #L'élève a déjà voté
            # messages.add_message(request, messages.ERROR, "Vous avez déjà voté !")
            peut_voter = False
            deja_vote = True
        elif request.POST:   
            liste = get_object_or_404(Liste, nom = request.POST['choix'])
            Vote.objects.create(liste = liste, eleve=request.user.get_profile())
            messages.add_message(request, messages.INFO, "A voté !")
            peut_voter = False
            deja_vote = True
    return render_to_response('bde/voter.html', {'peut_voter':peut_voter, 'deja_vote':deja_vote, 'liste1':liste1, 'liste2':liste2, 'debut_vote':debut_vote, 'fin_vote':fin_vote}, context_instance=RequestContext(request))
    
@login_required
@permission_required('bde.add_liste')
def resultats(request):
    listes = Liste.objects.filter(debut_vote__lte = datetime.datetime.now())
    liste1 = None
    liste2 = None
    if listes.count() >= 2: #Une election est commencée
        liste1 = listes[0]
        liste2 = listes[1]
        n_votes_1 = Vote.objects.filter(liste = liste1).count()
        n_votes_2 = Vote.objects.filter(liste = liste2).count()
    return render_to_response('bde/resultats.html', {'liste1':liste1, 'liste2':liste2, 'n_votes_2':n_votes_2, 'n_votes_1':n_votes_1}, context_instance=RequestContext(request))

@login_required
def palums(request):
    """
        La page des Palums
    """
    liste_palums = Palum.objects.order_by('-date')
    liste_palums_1A = liste_palums.filter(annee=1)
    liste_palums_2A = liste_palums.filter(annee=2)
    liste_palums_3A = liste_palums.filter(annee=3)
    return render_to_response('bde/palums.html', {'liste_palums_1A': liste_palums_1A, 'liste_palums_2A': liste_palums_2A, 'liste_palums_3A': liste_palums_3A}, context_instance=RequestContext(request))

@login_required
def palums_json(request):
    """
        Sérialisation au format JSON de la liste des Palums
    """
    liste_palums = Palum.objects.all()
    response = HttpResponse(mimetype='application/json')
    response.write(json.dumps([{
            'annee': p.annee,
            'fichier': p.fichier.url,
            'date': p.date
        } for p in liste_palums]))
    return response

@login_required
def offre_stage(request):
    return render_to_response('bde/offre_stage.html', {}, context_instance=RequestContext(request))

@login_required
def voeux_parrainage(request):
    parrain = request.user.get_profile()
    deuxA = parrain.annee()==2 #pour savoir si le parrain est bien en 2A et s'il a accès à la page du parrainage
    dejaVote=ParrainageVoeux.objects.filter(parrain=request.user).exists() # true si le parrain a déjà voté
    votesOuverts=False #Si les votes sont fermés
    if request.method == 'POST': 
        form = ParrainageVoeuxForm(request.POST,request.FILES) 
        if form.is_valid(): 
            if dejaVote: 
                ParrainageVoeux.objects.filter(parrain=request.user).delete() 
            fillot_n1 = form.cleaned_data['fillot_n1']
            fillot_n2 = form.cleaned_data['fillot_n2']
            fillot_n3 = form.cleaned_data['fillot_n3']
            fillot_n4 = form.cleaned_data['fillot_n4']
            fillot_n5 = form.cleaned_data['fillot_n5']
            fillot_n6 = form.cleaned_data['fillot_n6']
            fillot_n7 = form.cleaned_data['fillot_n7']
            fillot_n8 = form.cleaned_data['fillot_n8']
            liste = [fillot_n1,fillot_n2,fillot_n3,fillot_n4,fillot_n5,fillot_n6,fillot_n7,fillot_n8]
            parrainage = form.save(commit=False)
            if parrainage.different_voeux(liste):# si les fillots sont bien tous différents
                parrainage.parrain=parrain
                parrainage.save()
                messages.add_message(request, messages.INFO, "Ton choix des fillots a bien été pris en compte.")
                return redirect('messages.views.index')
            else:
                messages.add_message(request, messages.ERROR, "Tu as choisi plusieurs fois le même fillot, tes voeux ont été supprimés.")
    else:
        form = ParrainageVoeuxForm()
    return render_to_response('bde/voeux_parrainage.html', {'form': form,'dejaVote':dejaVote,'deuxA':deuxA, 'votesOuverts':votesOuverts},context_instance=RequestContext(request))

@login_required
def visualiser_voeux_parrainage(request):
    parrain = request.user.get_profile()
    deuxA = parrain.annee()==2
    dejaVote=ParrainageVoeux.objects.filter(parrain=request.user).exists()
    if dejaVote:
        voeu = ParrainageVoeux.objects.filter(parrain=request.user)[0]
        fillot1= voeu.fillot_n1
        fillot2= voeu.fillot_n2
        fillot3= voeu.fillot_n3
        fillot4= voeu.fillot_n4
        fillot5= voeu.fillot_n5
        fillot6= voeu.fillot_n6
        fillot7= voeu.fillot_n7
        fillot8= voeu.fillot_n8
        return render_to_response('bde/visualiser_voeux_parrainage.html', {'dejaVote':dejaVote,'deuxA':deuxA,'fillot1':fillot1,'fillot2':fillot2,'fillot3':fillot3,'fillot4':fillot4,'fillot5':fillot5,'fillot6':fillot6,'fillot7':fillot7,'fillot8':fillot8},context_instance=RequestContext(request))
    return render_to_response('bde/visualiser_voeux_parrainage.html', {'dejaVote':dejaVote,'deuxA':deuxA},context_instance=RequestContext(request))

@permission_required('bde.add_parrainagevoeux')
@login_required
def voeux_parrainage_export(request):
    from django.template import loader, Context
    liste_voeux = ParrainageVoeux.objects.all()
    response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=export_voeux.csv'
    t = loader.get_template('bde/export_voeux.txt')
    c = Context({'liste_voeux': liste_voeux})
    response.write(t.render(c))
    return response

@permission_required('bde.add_parrainagevoeux')
@login_required
def voeux_parrainage_algo_export(request):
    from django.template import loader, Context
    import csv
    liste_voeux = ParrainageVoeux.objects.all()
    parrains=[]
    ligneParrain=[0]
    fillot=[]
    for voeu in liste_voeux:
        parrains.append(voeu.parrain)
        ligneParrain.append(voeu.parrain.user.username)
        if not voeu.fillot_n1 in fillot:
            fillot.append(voeu.fillot_n1)
        if not voeu.fillot_n2 in fillot:
            fillot.append(voeu.fillot_n2)
        if not voeu.fillot_n3 in fillot:
            fillot.append(voeu.fillot_n3)
        if not voeu.fillot_n4 in fillot:
            fillot.append(voeu.fillot_n4)
        if not voeu.fillot_n5 in fillot:
            fillot.append(voeu.fillot_n5)
        if not voeu.fillot_n6 in fillot:
            fillot.append(voeu.fillot_n6)
        if not voeu.fillot_n7 in fillot:
            fillot.append(voeu.fillot_n7)
        if not voeu.fillot_n8 in fillot:
            fillot.append(voeu.fillot_n8)
    response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=export_voeux_algo.csv'
    writer = csv.writer(response)
    writer.writerow(ligneParrain)

    for fil in fillot:
        ligne=[fil.user.username]
        for parrain in parrains:
            if ParrainageVoeux.objects.filter(parrain=parrain,fillot_n1=fil).exists():
                ligne.append(1)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n2=fil).exists():
                ligne.append(2)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n3=fil).exists():
                ligne.append(3)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n4=fil).exists():
                ligne.append(4)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n5=fil).exists():
                ligne.append(5)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n6=fil).exists():
                ligne.append(6)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n7=fil).exists():
                ligne.append(7)
            elif ParrainageVoeux.objects.filter(parrain=parrain,fillot_n8=fil).exists():
                ligne.append(8)
            else : #on ne souhaite pas avoir ce fillot
                ligne.append(15) 
        writer.writerow(ligne)
    return response
