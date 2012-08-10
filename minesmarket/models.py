# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms

class Produit(models.Model):
 CATEGORIES = ( #A changer par une classe ?
  ('Boissons', 'Boissons'),
  ('Sauces', 'Sauces'),
  ('Conserves', 'Conserves'),
 )

 nom = models.CharField(max_length=80)
 description = models.CharField(max_length=300)
 categorie = models.CharField(max_length=50, choices=CATEGORIES)
 image = models.ImageField(upload_to='minesmarket', blank=True)
 reference = models.CharField(max_length=20)
 pack = models.IntegerField()
 prix_achat = models.DecimalField(max_digits=4, decimal_places=2)
 prix_vente = models.DecimalField(max_digits=4, decimal_places=2)
   
 def __unicode__(self):
  return self.nom
   
class Commande(models.Model):
 eleve = models.ForeignKey(UserProfile)
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
 
 def __unicode__(self):
  if self.commande.fermee:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom + ' (fermee)'
  else:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom
  