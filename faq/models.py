#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
	nom = models.CharField(max_length=255)
	email = models.EmailField()
	objet = models.CharField(max_length=255)
	contenu = models.TextField()
	date = models.DateTimeField()
	
	class Meta:
		ordering = ['-date']
	
	def __unicode__(self):
		return self.objet
	

class Reponse(models.Model):
	question = models.OneToOneField(Question, related_name = "reponse")
	eleve = models.ForeignKey(User)
	contenu = models.TextField()
	date = models.DateTimeField()
    
	class Meta:
		ordering = ['-date']
	
	def __unicode__(self):
		return str(self.eleve) + ' -> ' + str(self.question)
