from django.db import models
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
	vendorStreet1 = models.CharField(max_length=50, blank=True)
	vendorStreet2 = models.CharField(max_length=50, blank=True)
	vendorPostal = models.CharField(max_length=10, blank=True)
	vendorCity = models.CharField(max_length=50, blank=True)
	vendorCountry = models.CharField(max_length=25, blank=True)
	vendorLatitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
	vendorLongitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True)
	vendorRibName = models.CharField(max_length=50)
	vendorRibBanque = models.CharField(max_length=5)
	vendorRibGuichet = models.CharField(max_length=5)
	vendorRibCompte = models.CharField(max_length=11)
	vendorRibClef = models.CharField(max_length=2)