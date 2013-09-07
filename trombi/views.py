#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from trombi.models import UserProfile, Question, Reponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from trombi.tools import update_profile
from association.models import Adhesion
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.conf import settings
from urllib import urlretrieve
import subprocess
import vobject
import Image
import json
import os

@login_required
def trombi(request):
    """Le trombinoscope des élèves des Mines. N'affique que les 1A, 2A, 3A, et 4A"""
    promo_max = UserProfile.premiere_annee() - 3
    mineur_list = mineur_list.filter(promo__gte = promo_max)
    return render_to_response('trombi/index.html', {'mineur_list': mineur_list}, context_instance = RequestContext(request))

@login_required
def trombi_json(request):
    """Sérialisation JSON de tous les élèves, pour les applis mobiles"""
    mineur_list = UserProfile.objects.all()
    response = HttpResponse(mimetyp = 'application/json')
    response.write(simplejson.dumps([{
            'username': m.user.username,
            'first_name': m.first_name.title(),
            'last_name': m.last_name.title(),
            'promo': m.promo,
            'phone': m.phone
        } for m in mineur_list]))
    return response

@login_required
def detail(request, mineur_login):
    """Page de profil d'un élève"""
    mineur = get_object_or_404(UserProfile, user__username = mineur_login)
    assoces = Adhesion.objects.filter(eleve = mineur)
    liste_questions = Question.objects.all()
    liste_reponses = mineur.reponses.all()
    return render_to_response('trombi/detail.html', {'mineur': mineur.user, 'assoces': assoces, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses},context_instance=RequestContext(request))

def detail_json(request, mineur_login):
    """Sérialisation au format JSON des infomations d'un élève"""
    mineur = get_object_or_404(UserProfile, user__username = mineur_login)   
    assoces = Adhesion.objects.filter(eleve = mineur)
    response = HttpResponse(mimetype='application/json')
    response.write(simplejson.dumps({
        'username': mineur.user.username,
        'first_name': mineur.first_name.title(),
        'last_name': mineur.last_name.title(),
        'email': mineur.user.email,
        'promo': mineur.promo,
        'phone': mineur.phone,
        'chambre': mineur.chambre,
        'birthday': str(mineur.birthday),
        'co': [eleve.user.username for eleve in mineur.co.all()],
        'parrains': [eleve.user.username for eleve in mineur.parrains.all()],
        'fillots': [eleve.user.username for eleve in mineur.fillots.all()],
        'assoces': [{'pseudo': a.association.pseudo, 'nom': str(a.association), 'role': a.role} for a in assoces]
    }))
    return response

@csrf_exempt    
def token(request):
    """Page pour récupérer la token d'identification par CRSF"""
    return render_to_response('trombi/token.html', {},context_instance=RequestContext(request))

@login_required
def profile(request):
    """Page de profil de l'utilisateur"""
    return detail(request,request.user.username)
    
@csrf_exempt
def octo_update(request):
    """
        Mise à jour de tous les soldes octo/biéro

        Cette page est appelée par le site de l'octo, hébergé par le rézal.
        Le serveur envoie une requête POST sur cette page tous les jours à 
        midi pour mettre à jour les données des soldes.

    """
    json_octo = json.loads(request.POST.get('clients_bar', '[]'))
    for eleve in json_octo:
        try:
            profile = UserProfile.objects.get(user__username = eleve['login'])
            profile.solde_octo = eleve['solde_octo']
            profile.solde_biero = eleve['solde_biero']    
            profile.save()
        except UserProfile.DoesNotExist:                
            pass
    return HttpResponse('OK')

@login_required
def edit(request):
    """Mise à jour des informations d'un profil"""
    mineur = request.user.get_profile()
    if request.method == 'POST':
        update_profile(mineur, surnom=request.POST['surnom'], phone=request.POST['phone'], chambre=request.POST['chambre'], option=request.POST['option'], co= request.POST.getlist('co'), parrains=request.POST.getlist('parrains'), fillots=request.POST.getlist('fillots'))
        # Le profil a été mis a jour, on update les questions
        for question in Question.objects.all():
            try:
                reponse_user = mineur.reponses.get(question=question)
                reponse_user.contenu = request.POST['question_'+str(question.id)]
                reponse_user.save()
            except Reponse.DoesNotExist:                
                reponse_user = Reponse.objects.create(question=question, contenu=request.POST['question_'+str(question.id)])
                reponse_user.save()
                mineur.reponses.add(reponse_user)      
        mineur.save()
        return redirect('profile')
    else:
        autres_eleves = UserProfile.objects.exclude(id = mineur.id)
        promo_superieure = UserProfile.objects.filter(promo = mineur.promo-1)
        promo_inferieure = UserProfile.objects.filter(promo = mineur.promo+1)
        liste_questions = Question.objects.all()
        liste_reponses = mineur.reponses.all()
        return render_to_response('trombi/edit.html', {'mineur': mineur.user, 'promo_inferieure': promo_inferieure, 'promo_superieure': promo_superieure, 'autres_eleves': autres_eleves, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses}, context_instance=RequestContext(request))

@login_required
def get_vcf(request):
    result = ""
    for user_profile in UserProfile.objects.all():
        card = vobject.vCard()
        card.add('n') 
        card.add('fn')
        card.add('tel')
        card.add('adr')
        card.add('email')
        card.email.value = user_profile.user.email
        card.adr.value = vobject.vcard.Address(street=user_profile.chambre)
        card.n.value = vobject.vcard.Name(family=user_profile.last_name,given=user_profile.first_name)
        card.fn.value = user_profile.first_name + ' ' + user_profile.last_name
        card.tel.value = user_profile.phone
        card.tel.type_param = 'cell'
        result += card.serialize()
        response = HttpResponse(content_type="text/vcard; charset=utf-8")
        response['charset'] = "utf-8"
        response.write(result)
        return response

@login_required
def separation(request):
    eleves = UserProfile.objects.all()
    result = []
    recherche = False
    if request.method == 'POST':
        recherche = True
        start = UserProfile.objects.get(user__username = request.POST.get('start_username', ''))
        end = UserProfile.objects.get(user__username = request.POST.get('end_username', ''))        
        result = UserProfile.BFS(start, end)
    result_string = chemin_to_html(result)
    return render_to_response('trombi/separation.html', {'eleves': eleves, 'result':result, 'result_string':result_string, 'recherche':recherche},context_instance=RequestContext(request))

def chemin_to_html(chemin):
    if chemin:        
        chemin_string = '<a href = "'+chemin[0].get_absolute_url()+'">'+chemin[0].first_name+' '+chemin[0].last_name+'</a>'
        for i in range(len(chemin)-1):
            chemin_string = chemin_string + ', ' + chemin[i].relation_avec(chemin[i+1]) + ' de ' + '<a href = "'+chemin[i+1].get_absolute_url()+'">'+chemin[i+1].first_name+' '+chemin[i+1].last_name+'</a>'
    else:
        chemin_string = "Aucun chemin existant"
    return chemin_string

import Image, ImageDraw
def separation_graphe(request):
    chemin = request.GET.get('chemin','')
    liste_eleves = [UserProfile.objects.get(user__username = username) for username in chemin.split(',')]
    
    largeur = 500
    hauteur = 375
    im = Image.new('RGBA', (largeur, hauteur), (0, 0, 0, 0)) # Create a blank image
    draw = ImageDraw.Draw(im)
    lines = []
    promo_min = min([eleve.promo for eleve in liste_eleves])
    promo_max = max([eleve.promo for eleve in liste_eleves])
    marge=30
    deltax = (largeur-2*marge)/len(liste_eleves)
    deltay = (hauteur-2*marge)/(promo_max-promo_min)
    x = 0
    rayon_cercles = 8-2*(promo_max-promo_min)
    hauteur_traits = 8-2*(promo_max-promo_min)
    for eleve in liste_eleves:
        lines.append((marge + x, marge + (eleve.promo-promo_min)*deltay))
        lines.append((marge + x + deltax, marge + (eleve.promo-promo_min)*deltay))
        #draw.ellipse((marge + (2*x+deltax)/2 - rayon_cercles, marge + (eleve.promo-promo_min)*deltay-rayon_cercles, marge + (2*x+deltax)/2 + rayon_cercles, marge + (eleve.promo-promo_min)*deltay+rayon_cercles), fill="black")
        draw.line([(marge + x, marge + (eleve.promo-promo_min)*deltay-hauteur_traits),(marge + x, marge + (eleve.promo-promo_min)*deltay+hauteur_traits)], fill="black")
        draw.line([(marge + x + deltax, marge + (eleve.promo-promo_min)*deltay-hauteur_traits),(marge + x + deltax, marge + (eleve.promo-promo_min)*deltay+hauteur_traits)], fill="black")
        x = x + deltax
    #lines = [(50, 0), (0, 40), (20, 100), (80, 100), (100, 40)]
    draw.line(lines, fill="black")
    for promo in range(promo_min, promo_max+1):
        draw.text((0, marge - 5 + (promo-promo_min)*deltay), 'P'+str(promo), fill="blue")
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write
from pygraph import *
def graphe_mine(request):
    gr = graph()
    liste_couleurs = ['red', 'royalblue4', 'forestgreen', 'goldenrod4', 'purple4']

    # On ajoute les noeuds
    for eleve in UserProfile.objects.all():
        couleur = eleve.promo 
        if not couleur:
            couleur = 0
        if not gr.has_node(eleve.user.username):
            gr.add_node(eleve.user.username, attrs=[('color', liste_couleurs[couleur % len(liste_couleurs)])])
    
    print gr.node_neighbors
    
    #On ajoute les aretes
    for eleve in UserProfile.objects.all():
        for eleve_co in eleve.co.all():
            if not gr.has_edge((eleve.user.username, eleve_co.user.username)):
                gr.add_edge((str(eleve.user.username), str(eleve_co.user.username)), attrs=[('color', 'grey23')])
        for eleve_parrain in eleve.parrains.all():
            if not gr.has_edge((eleve.user.username, eleve_parrain.user.username)):
                gr.add_edge((eleve.user.username, eleve_parrain.user.username))
    
    #Suppression des noeuds isoles
        for i in gr:
            if not gr.neighbors(i):
                gr.del_node(i) 
    
    dot = write(gr)
    chemin = os.path.join(settings.MEDIA_ROOT, "trombi")
    chemin_dot = os.path.join(chemin, "mine.dot")
    chemin_png = os.path.join(chemin, "mine.png")
    open(chemin_dot,'w').write(dot)
    subprocess.call(['dot.exe',"-Tpng",chemin_dot,"-o",chemin_png])
    url  = os.path.join(settings.MEDIA_URL, "trombi", "mine.png")
    return HttpResponseRedirect(url)