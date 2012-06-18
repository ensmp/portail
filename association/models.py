from django.db import models
from trombi.models import UserProfile
from django import forms


class Page(models.Model):
	titre = models.CharField(max_length=200)
	lien = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.titre

class Association(models.Model):
 nom = models.CharField(max_length=200)
 pseudo = models.CharField(max_length=20)
 membres = models.ManyToManyField(UserProfile, through='Adhesion')
 page = models.ForeignKey(Page, blank=True, null=True)

 
 def __unicode__(self):
  return self.nom

class Adhesion(models.Model):
	eleve = models.ForeignKey(UserProfile)
	association = models.ForeignKey(Association)
	role = models.CharField(max_length=64, blank=True)
	
	def __unicode__(self):
		return self.eleve.user.username + ' -> ' + self.association.nom

class AdhesionAjoutForm(forms.Form):

	eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
	role = forms.CharField(max_length=100, required=False)
	
	def __init__(self, association, *args, **kwargs):
		super(AdhesionAjoutForm, self).__init__(*args, **kwargs)
		self.fields['eleve'].queryset = UserProfile.objects.exclude(id__in = [m.id for m in association.membres.all()])
		
class AdhesionSuppressionForm(forms.Form):

	eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
	
	def __init__(self, association, *args, **kwargs):
		super(AdhesionSuppressionForm, self).__init__(*args, **kwargs)
		self.fields['eleve'].queryset = association.membres.all()
		