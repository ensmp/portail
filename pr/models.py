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
	
"""class DeuxA(models.Model):    
    nom = models.CharField(max_length=32)
    nbVotes = models.IntegerField(max_length=7)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom        
        
class Cesurien(models.Model):    
    nom = models.CharField(max_length=32)
    nbVotes = models.IntegerField(max_length=7)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom 

class Vote2A(models.Model):
    liste = models.ForeignKey(DeuxA)
    eleve = models.ForeignKey(UserProfile, related_name="votes_2A")
    
    def __unicode__(self):
        return self.eleve.user.username

class VoteCesurien(models.Model):
    liste = models.ForeignKey(Cesurien)
    eleve = models.ForeignKey(UserProfile, related_name="votes_Cesurien") 

    def __unicode__(self):
        return self.eleve.user.username"""

class Candidat(models.Model):    
    nom = models.CharField(max_length=32)
    nbVotes = models.IntegerField(max_length=7)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom  

class Vote(models.Model):
    liste = models.ForeignKey(Candidat)
    eleve = models.ForeignKey(UserProfile, related_name="votes")
    
    def __unicode__(self):
        return self.eleve.user.username
