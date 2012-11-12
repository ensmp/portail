#-*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from evenement.models import Evenement
from trombi.models import UserProfile
from association.models import Association

# Create your models here.
class EvenementPayant(Evenement):
	buypacker_dealId = models.IntegerField(unique=True)
	buypacker_dealPriceMin = models.FloatField()
	buypacker_dealSaleStart = models.DateField()
	buypacker_dealSaleEnd = models.DateField()
	buypacker_dealUrl = models.URLField()
   
class Transaction(models.Model):
	eleve = models.ForeignKey(UserProfile)
	evenement = models.ForeignKey(EvenementPayant)
	transactionId = models.IntegerField()
	transactionMethod = models.CharField(max_length=1)
	transactionPrice = models.FloatField()
	transactionCreatedOn = models.DateField()
	
class CompteBancaire(models.Model):
	association = models.ForeignKey(Association)
	vendorStreet1 = models.CharField(max_length=50, blank=True, verbose_name="Numéro et rue")
	vendorStreet2 = models.CharField(max_length=50, blank=True, verbose_name="Complément d'adresse")
	vendorPostal = models.CharField(max_length=10, blank=True, verbose_name="Code Postal")
	vendorCity = models.CharField(max_length=50, blank=True, verbose_name="Ville")
	vendorCountry = models.CharField(max_length=25, blank=True, verbose_name="Pays")
	#vendorLatitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Latitude")
	#vendorLongitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Longitude")
	vendorRibName = models.CharField(max_length=50, verbose_name="Nom RIB")
	vendorRibBanque = models.CharField(max_length=5, verbose_name="Banque RIB")
	vendorRibGuichet = models.CharField(max_length=5, verbose_name="Guichet RIB")
	vendorRibCompte = models.CharField(max_length=11, verbose_name="Compte RIB")
	vendorRibClef = models.CharField(max_length=2, verbose_name="Clef RIB")
	
class CompteBancaireForm(ModelForm):
	class Meta:
		model = CompteBancaire
		exclude = ('association')