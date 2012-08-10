# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile

# Une �tude JuMP
class Etude(models.Model):
	titre = models.CharField(max_length=256)
	promo = models.IntegerField() #La promo concern�e par l'�tude. A CHANGER (il peut y en avoir plusieurs ...)
	description = models.TextField()
	contact = models.ForeignKey(UserProfile) #La personne � la JuMP charg�e du suivi de l'�tude
	date = models.DateTimeField(auto_now_add=True)
	requests = models.ManyToManyField(UserProfile,related_name='+', blank=True, null=True) #Les �l�ves int�ress�s par l'�tude
	encours = models.BooleanField() #Si l'�tude est en cours de r�alisation
	
	def __unicode__(self):
		return self.titre