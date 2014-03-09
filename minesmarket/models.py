# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms

class Produit(models.Model):
 CATEGORIES = (
  ('Boissons', 'Boissons'),
  ('Condiments/Sauces', 'Condiments/Sauces'),
  ('Conserves', 'Conserves'),
  (u'Petit D\xe9jeuner', 'Petit Déjeuner'),
  ('Bouffe!', 'Bouffe!'),
  (u'Th\xe9/Caf\xe9', 'Thé/Café'),
  ('Confiseries','Confiseries'),
  ('Gateaux/Biscottes','Gateaux/Biscottes'),
  ('Non Alimentaire', 'Non Alimentaire')
 )

 nom = models.CharField(max_length=80)
 volume = models.CharField(max_length=80)
 categorie = models.CharField(max_length=50, choices=CATEGORIES)
 image = models.ImageField(upload_to='minesmarket', blank=True)
 ref = models.CharField(max_length=20)
 prix_vente = models.DecimalField(max_digits=4, decimal_places=2)
 metro = models.BooleanField(default=False)
   
 def __unicode__(self):
  return self.nom
   
class Commande(models.Model):
 eleve = models.ForeignKey(UserProfile)
 validee = models.BooleanField()
 fermee = models.BooleanField()
 livree = models.BooleanField()
 date_fermeture = models.DateField(blank=True, null=True)
 
 def __unicode__(self):
  if self.fermee:
   return 'commande de ' + self.eleve.user.username + ' (fermee)'
  else:
   return 'commande de ' + self.eleve.user.username


 def total(self):
  liste_achats = Achat.objects.filter(commande__id = self.id)
  total = 0
  for achat in liste_achats:
    total = total + achat.produit.prix_vente*achat.quantite 
  return total

class Achat(models.Model):
 produit = models.ForeignKey(Produit)
 quantite = models.IntegerField() 
 commande = models.ForeignKey(Commande)
 
 def __unicode__(self):
  if self.commande.fermee:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom + ' (fermee)'
  else:
   return self.commande.eleve.user.username + ' -> ' + str(self.quantite) + ' ' + self.produit.nom
  
class UpdateSoldeForm(forms.Form):
 eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
 credit = forms.FloatField()