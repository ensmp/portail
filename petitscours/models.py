# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

#Une proposition de petit cours
class PetitCours(models.Model):
	title = models.CharField(max_length=256)
	contact = models.CharField(max_length=256) #Num�ro de t�l�phone ?
	date_added = models.DateTimeField(auto_now_add=True)
	date_given = models.DateTimeField(auto_now_add=True)
	visible = models.BooleanField()
	niveau = models.CharField(max_length=256)
	matiere = models.CharField(max_length=256)
	description = models.CharField(max_length=512)
	requests = models.ManyToManyField(User,related_name='+', blank=True, null=True) #Les demandes 
	
	address = models.CharField(max_length=500, null=True) #Adresse � Paris (via l'API Google Maps)
	latitude = models.FloatField(null=True) #r�cup�r�e dynamiquement via l'API Google Maps
	longitude = models.FloatField(null=True) #r�cup�r�e dynamiquement via l'API Google Maps

	visible.default = True

	def __unicode__(self):
		return self.title
		
	#Met � jour la position GPS du petit cours. Appel� depuis l'API Google Maps.
	def update_location(self, lat, lon):
		self.latitude = lat
		self.longitude = lon
