from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from trombi.models import UserProfile, Question, Reponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from trombi.tools import update_profile
from association.models import Adhesion
from django.http import Http404, HttpResponse
from django.utils import simplejson
from urllib import urlretrieve
import Image

@login_required
def index(request):
	mineur_list = UserProfile.objects.order_by('-promo','last_name')
	return render_to_response('trombi/index.html', {'mineur_list': mineur_list},context_instance=RequestContext(request))

def index_json(request):
	mineur_list = User.objects.order_by('username')
	response = HttpResponse(mimetype='application/json')
	response.write(simplejson.dumps([{
			'username': m.username,
			'first_name': m.get_profile().first_name,
			'last_name': m.get_profile().last_name,
			'promo': m.get_profile().promo
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
		'first_name': profile.first_name,
		'last_name': profile.last_name,
		'email': mineur.email,
		'promo': profile.promo,
		'phone': profile.phone,
		'chambre': profile.chambre,
		'birthday': str(profile.birthday),
		'co': profile.co.username if profile.co else None,
		'parrain': profile.parrain.username if profile.parrain else None,
		'fillot': profile.fillot.username if profile.fillot else None,
		'assoces': [{'pseudo': a.association.pseudo, 'nom': str(a.association), 'role': a.role} for a in assoces]
	}))
	return response

	
def token(request):
	return render_to_response('trombi/token.html', {},context_instance=RequestContext(request))

@login_required
def image(request,mineur_login):
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
		update_profile(request,mineur_login,phone=request.POST['phone'],promo=request.POST['promo'],chambre=request.POST['chambre'],option=request.POST['option'])
		# le profil a ete cree/ mis a jour, on update les questions
		profile = request.user.get_profile()
		for question in Question.objects.all():
			try:
				reponse_user = profile.reponses.get(question__id=question.id)
			except Reponse.DoesNotExist:
				reponse_user = Reponse.objects.create(question=question, contenu=request.POST['question_'+str(question.id)])
				profile.reponses.add(reponse_user)
				reponse_user.save()
				profile.save()
			reponse_user.contenu = request.POST['question_'+str(question.id)]
			reponse_user.save()
		return redirect('/accounts/profile')
	else:
		mineur = get_object_or_404(UserProfile,user__username=mineur_login)
		assoces = Adhesion.objects.filter(eleve__user__username = mineur_login)
		liste_questions = Question.objects.all()
		liste_reponses = mineur.reponses.all()
		return render_to_response('trombi/edit.html', {'mineur': mineur.user, 'assoces': assoces, 'liste_questions': liste_questions, 'liste_reponses': liste_reponses},context_instance=RequestContext(request))
		