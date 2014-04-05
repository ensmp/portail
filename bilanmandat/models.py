# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django.db.models import Q
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes import generic


     

class QuestionBilan(models.Model):
    question = models.CharField(max_length=512)
    resultat = models.IntegerField()
    vu = models.BooleanField()    

    
    def __unicode__(self):
        return self.question

    def trouve(self):
        if (VoteBilan.objects.filter(questionBilan = self, reponse = self.resultat)):
            return True
        else :
            return False
		


        
class VoteBilan(models.Model):
    questionBilan = models.ForeignKey(QuestionBilan)
    eleve = models.ForeignKey(UserProfile)
    reponse = models.IntegerField(blank=False)
    
    def __unicode__(self):
        return self.eleve.user.username + ' -> ' + self.questionBilan.question