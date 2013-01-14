from django.db import models
from django import forms
import datetime

class Clip(models.Model):
	titre = models.CharField(max_length=100)
	lien = models.URLField()
	promo = models.IntegerField(default=lambda : datetime.date.today().year-2002)
	
	class Meta:
		ordering = ["-promo", "titre"]
		
	def __unicode__(self):
		return self.titre
	
	