# -*- coding: utf-8 -*-

from trombi.models import UserProfile
from django.contrib.auth.models import User
from trombi.models import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request,mineur,phone,promo,chambre,option):
	# TODO gérer si un user modifie le profil d'un autre (peut être dans views.py)
	if request.user.get_profile():
		profile = request.user.get_profile()
	else:
		profile = UserProfile.objects.create(user=request.user)
	profile.promo = promo
	profile.phone = phone
	profile.chambre = chambre
	profile.option = option
	profile.save()

def password_request(login):
	print "hello"