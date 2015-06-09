#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from trombi.models import UserProfile, Question, Reponse
from association.models import Adhesion, Association
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from trombi.tools import update_profile
from association.models import Adhesion
from django.http import Http404, HttpResponse
from django.utils import simplejson
from django.conf import settings
from urllib import urlretrieve
from bda.models import Instrument, Maitrise
from django.views.generic import CreateView, UpdateView, DeleteView
import subprocess
import vobject
import Image
import json
import os
from settings import SECRET_KEY_UPDATE
from django.forms import ModelForm


@login_required
def trombi(request):
    """Le trombinoscope des élèves des Mines. N'affique que les 1A, 2A, 3A, et 4A"""    
    mineur_list = UserProfile.objects.promos_actuelles(3)
    return render_to_response('trombi/trombi.html', {'mineur_list': mineur_list}, context_instance = RequestContext(request))
	
@login_required
def trombi_assos(request):
    """Le trombinoscope des élèves des Mines. N'affique que les 1A, 2A, 3A, et 4A"""    
    mineur_list = UserProfile.objects.promos_actuelles(2)
    adhesions = Adhesion.objects.all()
    assoces = Association.objects.all()
    return render_to_response('trombiassos/trombi.html', {'mineur_list': mineur_list,'assoces':assoces,'adhesions':adhesions}, context_instance = RequestContext(request))

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
    if request.user.get_profile().en_premiere_annee():
        assoces = assoces.exclude(association__is_hidden_1A = True)
    liste_questions = Question.objects.all()
    liste_reponses = mineur.reponses.all()
    return render_to_response('trombi/detail.html', {'mineur': mineur.user, 'assoces': assoces, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses},context_instance=RequestContext(request))

@login_required
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
    """Page pour récupérer la token d'identification par CSRF"""
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
    json_octo = json.loads(request.POST.get('clients_bar', []))
    clef=request.POST.get('clef','')
    if clef==SECRET_KEY_UPDATE :
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
        return redirect(profile)
    else:
        autres_eleves = UserProfile.objects.exclude(id = mineur.id)
        promo_superieure = UserProfile.objects.filter(promo = mineur.promo-1)
        promo_inferieure = UserProfile.objects.filter(promo = mineur.promo+1)
        liste_questions = Question.objects.all()
        liste_reponses = mineur.reponses.all()
        #liste_instruments = Instrument.all()
        #liste_maitrise = Maitrise.all()
        return render_to_response('trombi/edit.html', {'mineur': mineur.user, 'promo_inferieure': promo_inferieure, 'promo_superieure': promo_superieure, 'autres_eleves': autres_eleves, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses}, context_instance=RequestContext(request))
        #return render_to_response('trombi/edit.html', {'mineur': mineur.user, 'promo_inferieure': promo_inferieure, 'promo_superieure': promo_superieure, 'autres_eleves': autres_eleves, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses, 'instruments'=liste_instruments, 'maitrises'=liste_maitrise}, context_instance=RequestContext(request))




@login_required
def edit_instruments(request):
    """Mise à jour des instruments maitrisés d'un profil"""
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
        return redirect(profile)
    else:
        return render_to_response('trombi/edit_instruments.html', {'mineur': mineur.user}, context_instance=RequestContext(request))


class ModifierMaitriseForm(ModelForm):
    class Meta:
        model = Maitrise
        exclude = ('eleve',)


class AjouterMaitrise(CreateView):
    model = Maitrise
    form_class = ModifierMaitriseForm
    template_name = 'trombi/form_instruments.html'
    success_url = reverse_lazy('trombi.views.edit_instruments')

    def form_valid(self, form):
        maitrise = Maitrise()
        maitrise.eleve = get_object_or_404(UserProfile,user=self.request.user)
        maitrise.instrument = form.cleaned_data['instrument']
        maitrise.niveau = form.cleaned_data['niveau']
        maitrise.save()
        return render_to_response('trombi/edit_instruments.html', {'mineur': self.request.user}, context_instance=RequestContext(self.request))


class ModifierMaitrise(UpdateView):
    model = Maitrise
    form_class = ModifierMaitriseForm
    template_name = 'trombi/form_instruments.html'
    success_url = reverse_lazy('trombi.views.edit_instruments')

class SupprimerMaitrise(DeleteView):
    model = Maitrise
    template_name = 'trombi/form_instruments.html'
    success_url = reverse_lazy('trombi.views.edit_instruments')


@login_required
def get_vcf(request):
    """Contacts au format VCF"""
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
    """Le plus court chemin séparant deux élèves"""
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
    """
        Effectue un rendu en code HTML d'une liste d'élèves en précisant les
        relations entre deux élèves successifs.
    """
    if chemin:        
        chemin_string = '<a href = "'+chemin[0].get_absolute_url()+'">'+chemin[0].first_name+' '+chemin[0].last_name+'</a>'
        for i in range(len(chemin)-1):
            chemin_string = chemin_string + ', ' + chemin[i].relation_avec(chemin[i+1]) + ' de ' + '<a href = "'+chemin[i+1].get_absolute_url()+'">'+chemin[i+1].first_name+' '+chemin[i+1].last_name+'</a>'
    else:
        chemin_string = "Aucun chemin existant"
    return chemin_string

@login_required
def graphe_chemin(request):
    """
        Dessine le graphe de l'évolution des promos d'une liste d'élèves

        La liste des usernames est récupérée en POST.
    """
    import Image, ImageDraw
    chemin = request.GET.get('chemin','')
    liste_eleves = [UserProfile.objects.get(user__username = username) for username in chemin.split(',')]
    
    largeur = 500
    hauteur = 375
    im = Image.new('RGBA', (largeur, hauteur), (0, 0, 0, 0)) # Nouvelle image
    draw = ImageDraw.Draw(im)
    lines = []
    promo_min = min([eleve.promo for eleve in liste_eleves])
    promo_max = max([eleve.promo for eleve in liste_eleves])
    marge = 30
    deltax = (largeur-2*marge)/len(liste_eleves)
    deltay = (hauteur-2*marge)/(promo_max-promo_min)
    x = 0
    hauteur_traits = 8-2*(promo_max-promo_min)
    for eleve in liste_eleves:
        lines.append((marge + x, marge + (eleve.promo-promo_min)*deltay))
        lines.append((marge + x + deltax, marge + (eleve.promo-promo_min)*deltay))        
        draw.line([(marge + x, marge + (eleve.promo-promo_min)*deltay-hauteur_traits),(marge + x, marge + (eleve.promo-promo_min)*deltay+hauteur_traits)], fill="black")
        draw.line([(marge + x + deltax, marge + (eleve.promo-promo_min)*deltay-hauteur_traits),(marge + x + deltax, marge + (eleve.promo-promo_min)*deltay+hauteur_traits)], fill="black")
        x = x + deltax
    draw.line(lines, fill="black")
    for promo in range(promo_min, promo_max+1):
        draw.text((0, marge - 5 + (promo-promo_min)*deltay), 'P'+str(promo), fill="blue")
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response

def ajouter_relation(gr, eleve1, eleve2):
        liste_couleurs = ['purple4', 'goldenrod4', 'royalblue4', 'forestgreen', 'red']
        try:
            couleur = eleve1.promo if eleve1.promo else 0
            gr.add_node(str(eleve1.user), attrs=[('color', liste_couleurs[couleur % len(liste_couleurs)]), ('style', 'filled'), ('fontcolor', 'white')])
        except:
            pass
        try:
            couleur = eleve2.promo if eleve2.promo else 0
            gr.add_node(str(eleve2.user), attrs=[('color', liste_couleurs[couleur % len(liste_couleurs)]), ('style', 'filled'), ('fontcolor', 'white')])
        except:
            pass
        try:    
            gr.add_edge((str(eleve1.user), str(eleve2.user)), attrs=[('color', 'grey23')])
        except:
            pass

@login_required
def graphe_mine(request):
    """
        Dessine une image du graphe des mineurs

        Les élèves sont les sommets du graphe, et les arêtes
        sont les relations parrain, fillot, co.
    """

    nombre_promos = int(request.GET.get("nombre_promos", 3))
    generate = bool(request.GET.get("generate", False))
    use_splines = bool(request.GET.get("splines", False))

    chemin = os.path.join(settings.MEDIA_ROOT, "trombi")
    chemin_dot = os.path.join(chemin, "graphe_mine"+str(nombre_promos)+".dot")
    chemin_png = os.path.join(chemin, "graphe_mine"+str(nombre_promos)+".png")

    if generate:
        from pygraph.classes.graph import graph
        from pygraph.classes.digraph import digraph
        from pygraph.algorithms.searching import breadth_first_search
        from pygraph.readwrite.dot import write
        from pygraph import *
        gr = graph()
    
        #On ajoute les aretes
        for eleve1 in UserProfile.objects.promos_actuelles(nombre_promos):
            for eleve2 in eleve1.co.all():
                if eleve2.annee() <= nombre_promos:
                    ajouter_relation(gr, eleve1, eleve2)
            for eleve2 in eleve1.parrains.all():
                if eleve2.annee() <= nombre_promos:
                    ajouter_relation(gr, eleve1, eleve2)
        
        #Suppression des noeuds isoles
            for i in gr:
                if not gr.neighbors(i):
                    gr.del_node(i) 
        
        dot = write(gr)
        
        # Utilisation de splines, pour éviter les overlap noeud/arêtes. Ralentit énormément les calculs.
        if use_splines:
            dot = dot[:17] + "splines=true; " + dot[17:]

        open(chemin_dot,'w').write(dot)     
        subprocess.call(["neato","-Tpng",chemin_dot,"-Goverlap=false","-o",chemin_png])
    url  = os.path.join(settings.MEDIA_URL, "trombi/graphe_mine"+str(nombre_promos)+".png")
    return render_to_response('trombi/graphe-mine.html', {'url': url}, context_instance=RequestContext(request))


