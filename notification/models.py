# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.exceptions import ObjectDoesNotExist 
from datetime import date, datetime, timedelta
from django.utils.encoding import smart_unicode, smart_str


class Notification(models.Model):
	destinataires = models.ManyToManyField(User, through = 'Envoi') #Les utilisateurs qui verront cette notification	
	message = models.CharField(max_length=512) #Le message lisible par l'utilisateur
	content_type = models.ForeignKey(ContentType) #Le type de contenu concerné
	object_id = models.PositiveIntegerField()
	content_object = generic.GenericForeignKey('content_type', 'object_id')	
	date = models.DateTimeField(auto_now_add=True)
	

	def __unicode__(self):
		str_objet=''
		if self.content_object:
			str_objet = smart_unicode(self.content_object)

		else:
			str_objet = '--Introuvable--'
		return str(self.content_type.model_class().__name__) + ' : ' + str_objet
	
	@property
	def est_recent(self):
		return (self.date.date() == date.today())

		
	def get_absolute_url(self):
		if not self.content_object:
			self.content_object = self.content_type.get_object_for_this_type(pk=self.object_id)

		if self.content_type.model_class().__name__ == 'Message':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Evenement':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'PetitCours':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Gallery':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Photo':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Video':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Affiche':
			return self.content_object.get_absolute_url()
		elif self.content_type.model_class().__name__ == 'Sondage':
			return '/sondages/valider/'
		elif self.content_type.model_class().__name__ == 'Comment':
			return self.content_object.content_object.get_absolute_url()
		else:
			return '#'
			
	def envoyer_multiple(self, users):
		for user in users:
			self.envoyer(user)
	
	def envoyer(self, user):
		Envoi.objects.create(notification = self, user = user)		
		
	def supprimer_destinataire(self, user):
		Envoi.objects.filter(notification = self, user = user).delete()
	
	def lire(self, user):
		Envoi.objects.filter(notification = self, user = user).update(lu = True)

		
class Envoi(models.Model):
	notification = models.ForeignKey(Notification)
	user = models.ForeignKey(User)
	lu = models.BooleanField() #Pour savoir si l'utilisateur a déjà vu la notification, ou pas.
	
	def lire(self):
		self.lu = True
		self.save()
		
	def est_lu(self): #Pour afficher differement une notification la premiere fois qu'elle est affichée
		if self.lu:
			return True
		else:
			self.lu = True
			self.save()
			return False