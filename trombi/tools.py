# -*- coding: utf-8 -*-

from trombi.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request,mineur,surnom,phone,chambre,option,co,parrains,fillots):
	if request.user.get_profile():
		profile = request.user.get_profile()
	else:
		profile = UserProfile.objects.create(user=request.user)
	profile.phone = phone
	profile.chambre = chambre
	profile.surnom = surnom
	profile.option = option    
		
	profile.co.clear()
	for co_name in co:
		try:
			profile.co.add(UserProfile.objects.get(user__username=co_name))
		except UserProfile.DoesNotExist:
			pass
	
	profile.parrains.clear()
	for parrain_name in parrains:
		try:			
			profile.parrains.add(UserProfile.objects.get(user__username=parrain_name))
		except UserProfile.DoesNotExist:
			pass
	
	profile.fillots.clear()
	for fillot_name in fillots:
		try:
			profile.fillots.add(UserProfile.objects.get(user__username=fillot_name))
		except UserProfile.DoesNotExist:
			pass
	profile.save()
    
	
def password_request(login):
	print "hello"