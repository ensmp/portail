# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, timedelta

class Question(models.Model):
    enonce = models.CharField(max_length=512)
    def __unicode__(self):
        return self.enonce

class Reponse(models.Model):
    question = models.ForeignKey(Question, related_name='+')
    contenu = models.CharField(max_length=512)
    
    def __unicode__(self):
        return str(self.question.id) + ' -> ' + self.contenu

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True)
    birthday = models.DateField(null=True)
    promo = models.IntegerField(null=True)
    option = models.CharField(max_length=128, blank=True)
    a_la_meuh = models.BooleanField(default=True)
    est_une_fille = models.BooleanField()

    chambre = models.CharField(max_length=128, blank=True)
    adresse_ailleurs = models.CharField(max_length=512, blank=True) 
    sports = models.CharField(max_length=512, blank=True)
    co = models.ForeignKey(User,related_name='+', blank=True, null=True)
    parrain = models.ForeignKey(User,related_name='+', blank=True, null=True)
    fillot = models.ForeignKey(User,related_name='+', blank=True, null=True)

    reponses = models.ManyToManyField(Reponse, blank=True)    
    
    class Meta:
        ordering = ['-promo','last_name']
    
    def __unicode__(self):
        return self.user.username
        
    def en_premiere_annee(self):
        from django.db.models import Max
        premiere_annee = UserProfile.objects.all().aggregate(Max('promo'))['promo__max']
        return (premiere_annee == self.promo)
    
  
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

