#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from trombi.models import UserProfile
from sondages.models import Sondage, Vote
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
    if Sondage.objects.filter(deja_paru = False, date_parution = datetime.date.today()).exists(): #Le sondage du jour a déjà été choisi
        sondage = get_object_or_404(Sondage, deja_paru = False, date_parution = datetime.date.today()) #On le récupère
        if Vote.objects.filter(sondage = sondage, eleve__user__username=request.user.username).exists(): #L'élève a déjà voté
            messages.add_message(request, messages.ERROR, "Vous avez déjà voté pour ce sondage")
        else:
            if request.POST['choix']:                
                Vote.objects.create(sondage = sondage, eleve=request.user.get_profile(), choix = int(request.POST['choix']))
                request.user.get_profile().update_sondages()
                messages.add_message(request, messages.INFO, "A voté !")
    if request.POST.get('next'):
        return HttpResponseRedirect(request.POST.get('next'))
    else:
        return HttpResponseRedirect('/')

    
@login_required
# Proposer un nouveau sondage
def proposer(request):
    if request.POST:
        if request.POST['question'] and request.POST['reponse1'] and request.POST['reponse2']:
            sondage = Sondage(auteur = request.user.get_profile(), question = request.POST['question'], reponse1 = request.POST['reponse1'], reponse2 = request.POST['reponse2'])
            sondage.save()
            sondage.envoyer_notification()
            messages.add_message(request, messages.INFO, "Votre sondage a bien été enregistré, il est maintenant en attente de validation.")            
        else:
            messages.add_message(request, messages.ERROR, "Vous devez spécifier une question et deux réponses.")
        return HttpResponseRedirect('/sondages/proposer/')
    else:
        return render_to_response('sondages/proposer.html',{},context_instance=RequestContext(request))

@permission_required('sondages.add_sondage')
# Valider un sondage proposé
def valider(request):
    if request.POST:
        sondage = get_object_or_404(Sondage, pk=request.POST['id'])
        sondage.autorise = True
        sondage.save()
        messages.add_message(request, messages.INFO, "Sondage validé")
        return HttpResponseRedirect('/sondages/valider/')
    else:
        liste_sondages = Sondage.objects.filter(autorise = False)
        return render_to_response('sondages/valider.html',{'liste_sondages':liste_sondages},context_instance=RequestContext(request))
        
@permission_required('sondages.add_sondage')
# Liste des sondages non validés
def en_attente(request):
    liste_sondages = Sondage.objects.filter(autorise = True, deja_paru = False)
    return render_to_response('sondages/en_attente.html',{'liste_sondages':liste_sondages},context_instance=RequestContext(request))

@permission_required('sondages.delete_sondage')
# Supprime un sondage
def supprimer(request):
    if request.POST:
        sondage = get_object_or_404(Sondage, pk=request.POST['id'])        
        sondage.delete()
        messages.add_message(request, messages.INFO, "Sondage supprimé")
    return HttpResponseRedirect('/sondages/valider/')
    
@login_required    
# Serialization JSON d'un sondage, pour les applis et le js. L'indice du sondage est anti-chronologique.
def detail_json(request, indice_sondage):
    sondage = Sondage.objects.filter(date_parution__isnull = False).filter(date_parution__lte = datetime.date.today()).order_by('-date_parution')[int(indice_sondage)]
    nombre_reponse = Vote.objects.filter(sondage = sondage).count()
    nombre_reponse_1 = Vote.objects.filter(sondage = sondage, choix = 1).count()
    nombre_reponse_2 = Vote.objects.filter(sondage = sondage, choix = 2).count()
    is_dernier = (int(indice_sondage) >= Sondage.objects.filter(date_parution__isnull = False).filter(date_parution__lte = datetime.date.today()).count() - 1)
    is_premier = (int(indice_sondage) <= 0)
    response = HttpResponse(mimetype='application/json')
    if is_premier and not Vote.objects.filter(sondage = sondage, eleve = request.user.get_profile()).exists(): #a vote
        response.write(json.dumps({
                'question': sondage.question,
                'reponse1': sondage.reponse1,
                'reponse2': sondage.reponse2,
                'date_parution': sondage.date_str(),
                'is_premier':is_premier,
                'is_dernier':is_dernier
            }))
    else: #n'a pas vote
        response.write(json.dumps({
                'question': sondage.question,
                'reponse1': sondage.reponse1,
                'reponse2': sondage.reponse2,
                'nombre_reponse': nombre_reponse,
                'nombre_reponse_1': nombre_reponse_1,
                'nombre_reponse_2': nombre_reponse_2,
                'date_parution': sondage.date_str(),
                'is_premier':is_premier,
                'is_dernier':is_dernier
            }))
    return response
    
@login_required    
# Les statistiques des sondages
def scores(request):    
    liste_eleves = UserProfile.objects.exclude(participations_sondages = 0)
    liste_eleves_c = liste_eleves.order_by('-score_victoires_sondages')[:10]
    liste_eleves_d = liste_eleves.order_by('-score_defaites_sondages')[:10]
    
    liste_eleves_c_semaine = UserProfile.objects.raw("SELECT trombi_userprofile.id as id, SUM(weight_score) as score FROM `sondages_vote` INNER JOIN sondages_sondage ON sondages_vote.sondage_id = sondages_sondage.id INNER JOIN trombi_userprofile ON trombi_userprofile.id = sondages_vote.eleve_id WHERE sondages_vote.choix = sondages_sondage.resultat GROUP BY sondages_vote.eleve_id ORDER BY score DESC LIMIT 10")
    liste_eleves_d_semaine = UserProfile.objects.raw("SELECT trombi_userprofile.id as id, SUM(weight_score) as score FROM `sondages_vote` INNER JOIN sondages_sondage ON sondages_vote.sondage_id = sondages_sondage.id INNER JOIN trombi_userprofile ON trombi_userprofile.id = sondages_vote.eleve_id WHERE sondages_vote.choix != sondages_sondage.resultat GROUP BY sondages_vote.eleve_id ORDER BY score DESC LIMIT 10")

    liste_eleves_participations = liste_eleves.order_by('-participations_sondages')[:10]
    return render_to_response('sondages/scores.html',{'liste_eleves_c':liste_eleves_c,'liste_eleves_d':liste_eleves_d, 'liste_eleves_c_semaine':liste_eleves_c_semaine, 'liste_eleves_d_semaine':liste_eleves_d_semaine, 'liste_eleves_participations':liste_eleves_participations},context_instance=RequestContext(request))