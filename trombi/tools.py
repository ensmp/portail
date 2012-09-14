# -*- coding: utf-8 -*-

from trombi.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request,mineur,phone,chambre,option,co,parrain,fillot):
	# TODO gérer si un user modifie le profil d'un autre (peut être dans views.py)
	if request.user.get_profile():
		profile = request.user.get_profile()
	else:
		profile = UserProfile.objects.create(user=request.user)
	profile.phone = phone
	profile.chambre = chambre
	profile.option = option
	try:
		profile.co = User.objects.get(username=co)
	except User.DoesNotExist:
		profile.co = None
	try:
		profile.parrain = User.objects.get(username=parrain)
	except User.DoesNotExist:
		profile.parrain = None
	try:
		profile.fillot = User.objects.get(username=fillot)
	except User.DoesNotExist:
		profile.fillot = None
	profile.save()

def password_request(login):
	print "hello"