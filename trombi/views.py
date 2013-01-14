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
from urllib import urlretrieve
import Image
import vobject

@login_required
def index(request):
    mineur_list = UserProfile.objects.order_by('-promo','last_name')
    return render_to_response('trombi/index.html', {'mineur_list': mineur_list},context_instance=RequestContext(request))

@login_required
def index_json(request):
    mineur_list = UserProfile.objects.order_by('-promo','last_name')
    response = HttpResponse(mimetype='application/json')
    response.write(simplejson.dumps([{
            'username': m.user.username,
            'first_name': m.first_name.title(),
            'last_name': m.last_name.title(),
            'promo': m.promo,
            'phone': m.phone
        } for m in mineur_list]))
    return response

@login_required
def detail(request,mineur_login):
    mineur = get_object_or_404(UserProfile,user__username=mineur_login)
    assoces = Adhesion.objects.filter(eleve__user__username = mineur_login)
    liste_questions = Question.objects.all()
    liste_reponses = mineur.reponses.all()
    return render_to_response('trombi/detail.html', {'mineur': mineur.user, 'assoces': assoces, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses},context_instance=RequestContext(request))

def detail_json(request,mineur_login):
    mineur = get_object_or_404(User,username=mineur_login)
    profile = mineur.get_profile()    
    assoces = Adhesion.objects.filter(eleve__user__username = mineur_login)
    response = HttpResponse(mimetype='application/json')
    response.write(simplejson.dumps({
        'username': mineur.username,
        'first_name': profile.first_name.title(),
        'last_name': profile.last_name.title(),
        'email': mineur.email,
        'promo': profile.promo,
        'phone': profile.phone,
        'chambre': profile.chambre,
        'birthday': str(profile.birthday),
        'co': [eleve.user.username for eleve in profile.co.all()],
        'parrains': [eleve.user.username for eleve in profile.parrains.all()],
        'fillots': [eleve.user.username for eleve in profile.fillots.all()],
        'assoces': [{'pseudo': a.association.pseudo, 'nom': str(a.association), 'role': a.role} for a in assoces]
    }))
    return response

@csrf_exempt    
def token(request):
    return render_to_response('trombi/token.html', {},context_instance=RequestContext(request))

@login_required
def photo(request,mineur_login):
    try:
        urlretrieve('https://sgs.mines-paristech.fr/prod/file/sgs/ensmp/20112012/photo/{}.jpg'.format(mineur_login), 'img.jpg')
        img = Image.open('img.jpg')
        resp = HttpResponse(mimetype='image/jpg')
        img.save(resp, 'JPEG')
        return resp
    except:
        return HttpResponse('err')

@login_required
def thumbnail(request,mineur_login):
    try:
        urlretrieve('https://sgs.mines-paristech.fr/prod/file/sgs/ensmp/20112012/photo/{}.jpg'.format(mineur_login), 'img.jpg')
        img = Image.open('img.jpg')
        img.thumbnail((44,44), Image.ANTIALIAS)
        resp = HttpResponse(mimetype='image/jpg')
        img.save(resp, 'JPEG')
        return resp
    except:
        return HttpResponse('err')

@login_required
def profile(request):
    return detail(request,request.user.username)

@login_required
def edit(request,mineur_login):
    if request.method == 'POST':
        update_profile(request,mineur_login,phone=request.POST['phone'],chambre=request.POST['chambre'],option=request.POST['option'], co=request.POST.getlist('co'), parrains=request.POST.getlist('parrains'), fillots=request.POST.getlist('fillots'))
        # le profil a ete cree/ mis a jour, on update les questions
        profile = request.user.get_profile()
        for question in Question.objects.all():
            try:
                reponse_user = profile.reponses.get(question__id=question.id)
                reponse_user.contenu = request.POST['question_'+str(question.id)]
                reponse_user.save()
            except Reponse.DoesNotExist:                
                reponse_user = Reponse.objects.create(question=question, contenu=request.POST['question_'+str(question.id)])
                profile.reponses.add(reponse_user)
                reponse_user.save()        
        profile.save()
        return redirect('/accounts/profile')
    else:
        mineur = get_object_or_404(UserProfile,user__username=mineur_login)
        autres_eleves = UserProfile.objects.exclude(id = request.user.get_profile().id)
        promo_superieure = UserProfile.objects.filter(promo = request.user.get_profile().promo-1)
        promo_inferieure = UserProfile.objects.filter(promo = request.user.get_profile().promo+1)
        liste_questions = Question.objects.all()
        liste_reponses = mineur.reponses.all()
        return render_to_response('trombi/edit.html', {'mineur': mineur.user, 'promo_inferieure': promo_inferieure, 'promo_superieure': promo_superieure, 'autres_eleves': autres_eleves, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses},context_instance=RequestContext(request))

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

from PIL import Image, ImageDraw
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