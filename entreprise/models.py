# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group, User

class Entreprise(models.Model):
    nom = models.CharField(max_length=200)
    lien = models.CharField(max_length=200)
    ordre = models.IntegerField(default=0)
    logo = models.ImageField(upload_to = 'logos')
    logo_height = models.PositiveSmallIntegerField(default=40, help_text = 'Ne pas toucher')
    logo_width = models.PositiveSmallIntegerField(default=40, help_text= 'Ne pas toucher')

    class Meta:
        ordering = ['ordre','nom']
 
    def __unicode__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        creation = self.pk is None #Creation de l'objet            
        super(Entreprise, self).save(*args, **kwargs)
         

