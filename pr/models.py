from django.db import models
from django import forms
from trombi.models import UserProfile
import datetime
from django.core.files import File
from datetime import date, datetime, timedelta
import subprocess
import os
from django import forms
from django.forms import ModelForm

class Clip(models.Model):
	titre = models.CharField(max_length=100)
	lien = models.URLField()
	promo = models.IntegerField(default=lambda : datetime.date.today().year-2002)
	
	class Meta:
		ordering = ["-promo", "titre"]
		
	def __unicode__(self):
		return self.titre
	

class Candidat(models.Model):    #C'est la petite zoe qui veut faire de la balancoire mais elle n'y arrive pas. 
    nom = models.CharField(max_length=32)   #Pourquoi 
    nbVotes = models.IntegerField(max_length=7) #Parce qu'elle n'a pas de bras ... merci 13Jougla
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom  

class Vote(models.Model):
    liste = models.ForeignKey(Candidat)
    eleve = models.ForeignKey(UserProfile, related_name="votes")
    
    def __unicode__(self):
        return 'vote de ' + self.eleve.user.username + ' pour ' + self.liste.nom
