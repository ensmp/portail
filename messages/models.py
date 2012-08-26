# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta
from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from notification.models import Notification
from django.db.models import Q



# Les messages d'association
class Message(models.Model):
	association = models.ForeignKey(Association)
	objet = models.CharField(max_length=300)
	contenu = models.TextField()
	date = models.DateTimeField(default=datetime.now(), blank=True)
	expediteur = models.ForeignKey(UserProfile) #L'élève qui a rédigé le message
	destinataire = models.ForeignKey(Association,related_name='message_destinataire', help_text="Si le message est public, laissez ce champ vide", blank=True, null=True) #L'assoce destinataire du message. Si null, le message est visible par tout le monde.
 
	lu = models.ManyToManyField(UserProfile,related_name='message_lu', blank=True) #Les élèves qui ont lu le message
	important = models.ManyToManyField(UserProfile,related_name='message_important', blank=True) #Les élèves qui ont classé le message comme important
  
	def __unicode__(self):
		return self.objet

	@property
	def est_recent(self):
		return (self.date.date() == date.today())
	
	def envoyer_notification(self):
		message = self.association.nom + ' a publie un nouveau message'
		notification = Notification(content_object=self, message=message)
		notification.save()
		if self.destinataire is None:
			notification.envoyer_multiple(self.association.suivi_par.all())
		else:
			recipients = self.association.suivi_par.all().filter(Q(userprofile__in = self.destinataire.membres.all) | Q(userprofile__in = self.association.membres.all))
			notification.envoyer_multiple(recipients)
				
	def save(self, *args, **kwargs):
		creation = self.pk is None #Creation de l'objet			
		super(Message, self).save(*args, **kwargs)
		if creation:			
			self.envoyer_notification()

	
class MessageForm(ModelForm):
	contenu = forms.CharField(widget=TinyMCE(attrs={'cols': 120, 'rows': 30}))

	class Meta:
		model = Message
		fields = ('destinataire', 'objet', 'contenu')