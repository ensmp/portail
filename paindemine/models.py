# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms

class Produit(models.Model):
 CATEGORIES = (
  ('Pain', 'Pain'),
  ('Viennoiseries', 'Viennoiseries')
 )

 nom = models.CharField(max_length=80)
 volume = models.CharField(max_length=80)
 categorie = models.CharField(max_length=50, choices=CATEGORIES)
 image = models.ImageField(upload_to='paindemine', blank=True)
 ref = models.CharField(max_length=20)
 prix_vente = models.DecimalField(max_digits=4, decimal_places=2)
   
 def __unicode__(self):
  return self.nom
   
class Commande(models.Model):
 eleve = models.ForeignKey(UserProfile,related_name='eleve')
 fermee = models.BooleanField()
 livree = models.BooleanField()
 date_fermeture = models.DateField(blank=True, null=True)
 
 def __unicode__(self):
  if self.fermee:
   return 'commande de ' + self.eleve.user.username + ' (fermee)'
  else:
   return 'commande de ' + self.eleve.user.username

class Achat(models.Model):
 produit = models.ForeignKey(Produit)
 quantite = models.IntegerField() 
 commande = models.ForeignKey(Commande)
 lundi = models.BooleanField(default=False,blank=True)
 mardi = models.BooleanField(default=False,blank=True)
 mercredi = models.BooleanField(default=False,blank=True)
 jeudi = models.BooleanField(default=False,blank=True)
 vendredi = models.BooleanField(default=False,blank=True)
 date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date de commande")
 
 def __unicode__(self):
  if self.commande.fermee:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom + ' (fermee)'
  else:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom

 def liste_jours(self):
  jours= ""
  if self.lundi:
    jours = jours + " lundi"
  if self.mercredi:
    jours = jours + " mercredi"
  if self.jeudi:
    jours = jours + " jeudi"
  return jours

 def nb_jours(self):
  jours= 0
  if self.lundi:
    jours = jours + 1
  if self.mercredi:
    jours = jours + 1
  if self.jeudi:
    jours = jours + 1
  return jours
  
class UpdateSoldeForm(forms.Form):
 eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
 credit = forms.FloatField(initial=0.0)
 debit = forms.FloatField(initial=0.0)