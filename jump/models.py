# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile

# Une étude JuMP
class Etude(models.Model):
	titre = models.CharField(max_length=256)
	promo = models.IntegerField() #La promo concernée par l'étude. A CHANGER (il peut y en avoir plusieurs ...)
	description = models.TextField()
	contact = models.ForeignKey(UserProfile) #La personne à la JuMP chargée du suivi de l'étude
	date = models.DateTimeField(auto_now_add=True)
	requests = models.ManyToManyField(UserProfile,related_name='+', blank=True, null=True) #Les élèves intéressés par l'étude
	encours = models.BooleanField() #Si l'étude est en cours de réalisation
	
	def __unicode__(self):
		return self.titre