# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from django.contrib.auth.models import Group, User


#Les pages personalisées des associations. On ne précise que le titre de la page et son url. La page en elle même est à implémenter dans une application ad-hoc.
class Page(models.Model):
	titre = models.CharField(max_length=200)
	lien = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.titre

#Une association, comme ensemble de membres
class Association(models.Model):
	nom = models.CharField(max_length=200)
	pseudo = models.CharField(max_length=20)
	groupe_permissions = models.OneToOneField(Group, blank=True, null=True)
	membres = models.ManyToManyField(UserProfile, through='Adhesion')
	page = models.ForeignKey(Page, blank=True, null=True)
	ordre = models.IntegerField(default=0)
 
	def __unicode__(self):
		return self.nom
 
	def save(self, *args, **kwargs):
		if not self.groupe_permissions: #On cree un groupe de permissions, si non-existant
			groupe = Group.objects.create(name=self.nom)
			self.groupe_permissions = groupe
		super(Association, self).save(*args, **kwargs) # Sauvegarde

#Permet de préciser l'appartenance d'un membre à une assoce, et en particulier son rôle.
class Adhesion(models.Model):
	eleve = models.ForeignKey(UserProfile)
	association = models.ForeignKey(Association)
	role = models.CharField(max_length=64, blank=True) #role dans l'association
	ordre = models.IntegerField(default = 0) #ordre d'apparition dans la page 'equipe' de l'assoce
	
	def __unicode__(self):
		return self.eleve.user.username + ' -> ' + self.association.nom

	def save(self, *args, **kwargs):
		self.association.groupe_permissions.user_set.add(self.eleve.user) #On ajoute l'eleve au groupe de permissions
		super(Adhesion, self).save(*args, **kwargs) # Sauvegarde
        
	def delete(self):
		self.association.groupe_permissions.user_set.remove(self.eleve.user) #On retire l'eleve du groupe de permissions
		super(Adhesion, self).delete()
	
		
		
		
		
		
		
		
		
		
		
#FORMULAIRES
class AdhesionAjoutForm(forms.Form):

	eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
	role = forms.CharField(max_length=100, required=False)
	#ordre = forms.ChoiceField(widget = forms.Select(), 
    #                 choices = ([('1','1'), ('2','2'),('3','3'), ]), initial='3', required = True,)
	
	def __init__(self, association, *args, **kwargs):
		super(AdhesionAjoutForm, self).__init__(*args, **kwargs)
		self.fields['eleve'].queryset = UserProfile.objects.exclude(id__in = [m.id for m in association.membres.all()])
		
class AdhesionSuppressionForm(forms.Form):

	eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
	
	def __init__(self, association, *args, **kwargs):
		super(AdhesionSuppressionForm, self).__init__(*args, **kwargs)
		self.fields['eleve'].queryset = association.membres.all()
	
	