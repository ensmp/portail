#-*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from association.models import Association, Adhesion
from datetime import date, datetime, timedelta

class Evenement(models.Model):
	"""
	    Un événement organisé par une association
	"""
	createur = models.ForeignKey(UserProfile, blank=True, null=True, help_text="L'élève qui a créé l'événement")
	association = models.ForeignKey(Association, null=False, help_text="L'association qui organise l'événement")
	titre = models.CharField(max_length=300)
	description =  models.TextField()
	date_debut = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="Date de début")
	date_fin = models.DateTimeField(default=datetime.now(), blank=True, verbose_name="Date de fin")
	lieu = models.CharField(max_length=300, blank = True)
	participants = models.ManyToManyField(UserProfile, related_name='evenement_participant', blank=True, help_text="La liste des participants")
	
	class Meta:
		ordering = ['-date_debut']
		verbose_name = "événement"
	
	def __unicode__(self):
		return self.titre
	
	def get_absolute_url(self):
		return self.association.get_absolute_url() + 'evenements/'
	
	def auteur(self):
		return self.association.nom
			
	def auteur_slug(self):
		return self.association.pseudo

	def peut_modifier(self, eleve):
		"""Renvoie vrai si un utilisateur a le droit de modifier l'événement"""
		return Adhesion.existe(eleve, self.association) # Si l'eleve est membre de l'assoce
