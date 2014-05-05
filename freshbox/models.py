# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms

  
class Commande(models.Model):
 eleve = models.ForeignKey(UserProfile,related_name='eleve_freshbox')
 validee = models.BooleanField()
 fermee = models.BooleanField()
 date_fermeture = models.DateField(blank=True, null=True)
 
 def __unicode__(self):
  if self.fermee:
   return 'commande de ' + self.eleve.user.username + ' (fermee)'
  else:
   return 'commande de ' + self.eleve.user.username

 
class UpdateSoldeForm(forms.Form):
 eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
 credit = forms.FloatField()