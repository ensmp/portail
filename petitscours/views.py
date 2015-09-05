# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from petitscours.models import PetitCours
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.template import RequestContext
from django.core.mail import send_mail
from django.contrib import messages
from django.utils import simplejson
from django.contrib.auth.models import User



@login_required
#Affiche les petits cours disponibles
def index(request):
    cours_list = PetitCours.objects.filter(visible=True).order_by('date_added')
    return render_to_response('petitscours/index.html',{'cours_list': cours_list},context_instance=RequestContext(request))
    
@login_required
#La liste des petits cours, sérialisée aux format JSON (pour les applis)
def index_json(request):
    cours_list = PetitCours.objects.filter(visible=True).order_by('date_added')
    response = HttpResponse(mimetype='application/json')
    response.write(simplejson.dumps([{
            'id': c.id,
            'titre': c.title,
            'niveau': c.niveau,
            'matiere': c.matiere,
            'description': c.description,            
            'latitude': c.latitude,
            'longitude': c.longitude,
            'adresse': c.address,
            'prenom': c.prenom,
            'disponibilite': c.disponibilite,
            'frequence': c.frequence,
        } for c in cours_list]))
    return response

@login_required
#Nouvelle requête d'un petit cours
def add_request(request,request_id):
    pc = PetitCours.objects.get(id=request_id)
    pc.requests.add(request.user)
    messages.add_message(request, messages.INFO, "C'est bien noté. Yapuka soudoyer le VP petits cours")

    return HttpResponseRedirect('/petitscours/')

@permission_required('petitscours.change_petitcours')
#Administration des petits cours
def admin(request):
    cours_list = PetitCours.objects.filter(visible=True).order_by('-date_added')
    archive_list = PetitCours.objects.order_by('-date_given').filter(visible=False)[:3]
    return render_to_response('petitscours/admin.html',{'cours_list': cours_list,'archive_list': archive_list},context_instance=RequestContext(request))
    
@permission_required('petitscours.change_petitcours')
#Historique des petits cours
def archive(request,page):
    page = int('0'+page)
    next = page+1
    previous = max(page-1,0)
    archive_list = PetitCours.objects.order_by('-date_given').filter(visible=False)[page*10:page*10+10]
    return render_to_response('petitscours/archive.html',{'archive_list': archive_list,'previous':previous,'next':next},context_instance=RequestContext(request))

@permission_required('petitscours.change_petitcours')
#Attribuer un petit cours à un élève
def give(request,id,mineur_login):
    pc = PetitCours.objects.get(id=id)
    eleve = User.objects.get(username = mineur_login)
    pc.date_given = datetime.now()
    pc.visible = False
    pc.attribue_a = eleve
    pc.save()
    send_mail('Attribution Petit Cours', 'Salut ! Tu viens de remporter le petit cours '+pc.title+'.\nPour le contacter: '+pc.contact+'.\nNiveau: '+pc.niveau+'\nMatiere: '+pc.matiere+'\nLieu: '+pc.address+'\nAutre: '+pc.description+ '\nPenses à informer le VP petits cours si jamais il y a un quelconque souci dans l\'attribution du petit cours.',[eleve.email])
    
    return HttpResponseRedirect('/petitscours/')

#Ajouter une nouvelle demande de petit cours.
def demander(request):
    if request.method == 'POST':
        pc = PetitCours()
        if request.user.is_authenticated():
            pc.poste_par = request.user
        else:
            pc.poste_par = None
        
        pc.title = request.POST.get('title', 'Cours de ' + request.POST['matiere'])
        pc.address=request.POST['address']
        pc.update_location(float(request.POST['lat']), float(request.POST['lng']))
        pc.contact=request.POST['contact']
        pc.matiere = request.POST['matiere']
        pc.niveau = request.POST['niveau']
        pc.description=request.POST['description']
        pc.prenom=request.POST['prenom']
        pc.disponibilite=request.POST['disponibilite']
        pc.frequence=request.POST['frequence']
        pc.save()        
        if request.is_ajax():
            return HttpResponse("OK")
        else:
            return render_to_response('petitscours/demander.html',context_instance=RequestContext(request))
    else:
        return render_to_response('petitscours/demander.html',context_instance=RequestContext(request))