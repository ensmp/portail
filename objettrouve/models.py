# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from datetime import datetime
from django import forms

# Un objet trouvé, ou un objet perdu
class ObjetTrouve(models.Model):
 eleve = models.ForeignKey(UserProfile) #l'élève qui a perdu ou trouvé l'objet
 trouve = models.BooleanField() #l'objet est trouvé si VRAI, et est perdu si FAUX
 description = models.CharField(max_length=300)
 lieu = models.CharField(max_length=200)
 date = models.DateTimeField(default=datetime.now, blank=True)
   
 def __unicode__(self):
  return self.description
  
#Formulaire d'ajout d'objet trouvé/perdu
class ObjetAjoutForm(forms.Form): 
	description = forms.CharField(max_length=300, required=True)
	trouve = forms.TypedChoiceField(label='Type', coerce=lambda x: bool(int(x)),
                   choices=((0, 'Perdu'), (1, 'Trouve')),
                   widget=forms.RadioSelect) #Un choix perdu/trouvé sous forme de Radio Buttons


	date = forms.DateField(initial=datetime.now)
	lieu = forms.CharField(max_length=200, required=True)

#Formulaire de suppression d'un objet trouvé/perdu
class ObjetSuppressionForm(forms.Form):

	objettrouve = forms.ModelChoiceField(label='Objet ',queryset=ObjetTrouve.objects.all())
	
	def __init__(self, user, *args, **kwargs):
		super(ObjetSuppressionForm, self).__init__(*args, **kwargs)
		self.fields['objettrouve'].queryset = ObjetTrouve.objects.filter(eleve=user)