#-*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta

# Un �v�nement organis� par une association
class Evenement(models.Model):
	is_personnel = models.BooleanField() #Les �venements personnels sont propres � l'�l�ve qui les cr�e, ind�pendament des associations
	createur = models.ForeignKey(UserProfile, blank=True, null=True) #El�ve qui a cr�� l'�venement
	association = models.ForeignKey(Association, blank=True, null=True) #L'association qui organise l'�venement
	titre = models.CharField(max_length=300)
	description =  models.TextField()
	date_debut = models.DateTimeField(default=datetime.now(), blank=True)
	date_fin = models.DateTimeField(default=datetime.now(), blank=True)
	lieu = models.CharField(max_length=300, blank = True)
	participants = models.ManyToManyField(UserProfile,related_name='evenement_participant', blank=True) #La liste des participants
	
	class Meta:
		ordering = ['-date_debut']
	
	def __unicode__(self):
		return self.titre
	
	def get_absolute_url(self):
		return '/associations/' + self.association.pseudo + '/evenements/'
	
	def date_debut_jour(self):
		return None
	
	def auteur(self):
		if self.is_personnel:
			return self.createur.user.username
		else:
			return self.association.nom

	def peut_modifier(self, eleve_user): #si un utilisateur a le droit de modifier l'�venement
		if self.is_personnel:			
			return (eleve_user.id == self.createur.user.id) #le createur
		else:
			return Adhesion.objects.filter(association=self.association, eleve=eleve_user).exists()#Si l'eleve est membre de l'assoce
