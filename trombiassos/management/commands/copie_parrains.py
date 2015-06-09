# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trombi.models import UserProfile
import json

class Command(BaseCommand):
	args = ''
	help = "Genere des mots de passe aleatoires pour tous les utilisateurs"

	def handle(self, *args, **options):	
		data = open('trombi.json').read() #opens the json file and saves the raw contents
		#print data
		jsonData = json.loads(data)
		for eleve in jsonData:
			try:
				profile = UserProfile.objects.get(pk = eleve['pk'])
				if eleve['fields']['parrain'] is not None:
					parrain = User.objects.get(pk = eleve['fields']['parrain'])
					profile.parrains.add(parrain.get_profile())
					print parrain.username + ' est le parrain de ' + profile.user.username
				
				if eleve['fields']['fillot'] is not None:
					fillot = User.objects.get(pk = eleve['fields']['fillot'])
					profile.fillots.add(fillot.get_profile())
					print fillot.username + ' est le fillot de ' + profile.user.username
				
				if eleve['fields']['co'] is not None:
					co = User.objects.get(pk = eleve['fields']['co'])
					profile.co.add(co.get_profile())
					print co.username + ' est le co de ' + profile.user.username	
			except UserProfile.DoesNotExist:
				pass
			except User.DoesNotExist:
				pass
			