from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from trombi.tools import update_profile
from association.models import Adhesion
from django.http import Http404

@login_required
def index(request):
	mineur_list = User.objects.order_by('username')
	return render_to_response('trombi/index.html', {'mineur_list': mineur_list},context_instance=RequestContext(request))

@login_required
def detail(request,mineur_login):
	mineur = get_object_or_404(User,username=mineur_login)
	assoces = Adhesion.objects.filter(eleve__user__username = mineur_login)
	return render_to_response('trombi/detail.html', {'mineur': mineur, 'assoces': assoces},context_instance=RequestContext(request))

@login_required
def profile(request):
	return detail(request,request.user.username)

@login_required
def edit(request,mineur_login):
	if request.method == 'POST':
		update_profile(request,mineur_login,phone=request.POST['phone'],promo=request.POST['promo'],chambre=request.POST['chambre'],option=request.POST['option'])
		return redirect('/accounts/profile')
	else:
		mineur = get_object_or_404(User,username=mineur_login)
		return render_to_response('trombi/edit.html', {'mineur': mineur},context_instance=RequestContext(request))