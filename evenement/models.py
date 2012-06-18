from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta

# Create your models here.
class Evenement(models.Model):
	association = models.ForeignKey(Association)
	titre = models.CharField(max_length=300)
	description =  models.TextField()
	date = models.DateTimeField(default=datetime.now(), blank=True)
	lieu = models.CharField(max_length=300)
	participants = models.ManyToManyField(UserProfile,related_name='evenement_participant', blank=True)
	is_billetterie = models.BooleanField()
	
	def __unicode__(self):
		return self.titre


class Reservation(models.Model):
	eleve = models.ForeignKey(UserProfile)
	acceptee = models.BooleanField()
	
	def __unicode__(self):
		return self.titre
	

	
class Billetterie(models.Model):
	evenement = models.ForeignKey(Evenement)
	prix = models.IntegerField()	
	reservations = models.ManyToManyField(Reservation,related_name='+', blank=True)
	date_fin_reservation = models.DateTimeField()
	nombre_places_total = models.IntegerField()
	
	def __unicode__(self):
		return self.evenement.titre
	
