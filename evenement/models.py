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
	is_billetterie = models.BooleanField() #Si l'�venement est associ� � une billeterie
	billetterie = models.ForeignKey('Billetterie', related_name='bloui', null = True, blank=True)
	
	def __unicode__(self):
		return self.titre
	
	def auteur(self):
		if self.is_personnel:
			return self.createur.user.username
		else:
			return self.association.nom

	def peut_modifier(self, eleve_user): #si un utilisateur a le droit de modifier l'�venement
		return (eleve_user.id == self.createur.user.id) #Pour l'instant il doit �tre cr�ateur. A changer eventuellement (permissions ...)

#Un �l�ve s'inscrit � une billeterie via une reservation. Un m�me �l�ve peut ainsi r�server plusieurs places (pour ses potes), mais elles ne seront peut �tre pas toutes accept�es.
class Reservation(models.Model):
	eleve = models.ForeignKey(UserProfile)
	acceptee = models.BooleanField() #Si la r�servation a �t� valid�e
	
	def __unicode__(self):
		return self.titre
	

#Impl�mente la billeterie d'un �venement
class Billetterie(models.Model):
	evenement = models.ForeignKey('Evenement', related_name='bla', null=True)
	prix = models.IntegerField()
	reservations = models.ManyToManyField(Reservation,related_name='+', blank=True)
	date_fin_reservation = models.DateTimeField(default=datetime.now(), blank=True)
	nombre_places_total = models.IntegerField()
	
	def __unicode__(self):
		return self.evenement.titre
	
