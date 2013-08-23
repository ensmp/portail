# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group, User
from evenement.models import Evenement
from datetime import date, datetime

class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    lien = models.URLField(max_length=200)
    ordre = models.IntegerField(default=0)
    logo = models.ImageField(upload_to = 'logos')
    logo_height = models.PositiveSmallIntegerField(default=40, editable = False)
    logo_width = models.PositiveSmallIntegerField(default=40, editable = False)

    class Meta:
        ordering = ['ordre','nom']
 
    def __unicode__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        creation = self.pk is None #Creation de l'objet            
        super(Entreprise, self).save(*args, **kwargs)
         
class EvenementEntreprise(models.Model):
    evenement = models.ForeignKey(Evenement)
    entreprise = models.ForeignKey(Entreprise)
    presence_1A = models.BooleanField()
    presence_2A = models.BooleanField()
    presence_3A = models.BooleanField()
    lien = models.URLField(max_length=200, blank=True,help_text= "Lien visible une fois l'evenement passé")

    def __unicode__(self):
        return self.evenement.titre

    @property
    def est_passe(self):
        return (self.evenement.date_debut.date() < date.today())
