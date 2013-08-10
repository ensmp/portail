# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from datetime import date, datetime, timedelta

class Liste(models.Model):    
    nom = models.CharField(max_length=32)
    couleur = models.CharField(max_length=7)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom        
        
class Vote(models.Model):
    liste = models.ForeignKey(Liste)
    eleve = models.ForeignKey(UserProfile, related_name="votes_liste")
    
    def __unicode__(self):
        return self.eleve.user.username

class EvenementEntreprise(models.Model):
    titre = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now)
    lieu = models.CharField(max_length=300, blank = True)
    presence_1A = models.BooleanField()
    presence_2A = models.BooleanField()
    presence_3A = models.BooleanField()
    lien = models.URLField(max_length=200, blank=True,help_text= "Lien visible une fois l'evenement passé")

    class Meta:
        ordering = ['date']
    
    def __unicode__(self):
        return self.titre