# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta

# Les messages d'association
class Message(models.Model):
 association = models.ForeignKey(Association)
 objet = models.CharField(max_length=300)
 contenu = models.TextField()
 date = models.DateTimeField(default=datetime.now(), blank=True)
 expediteur = models.ForeignKey(UserProfile) #L'élève qui a rédigé le message
 destinataire = models.ForeignKey(Association,related_name='message_destinataire', blank=True, null=True) #L'assoce destinataire du message. Si null, le message est visible par tout le monde.
 
 lu = models.ManyToManyField(UserProfile,related_name='message_lu', blank=True) #Les élèves qui ont lu le message
 important = models.ManyToManyField(UserProfile,related_name='message_important', blank=True) #Les élèves qui ont classé le message comme important
  
 def __unicode__(self):
  return self.objet

 @property
 def est_recent(self):
    return (self.date.date() == date.today())
