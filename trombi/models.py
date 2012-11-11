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
    co = models.ManyToManyField('self', symmetrical = True, blank=True, null=True)
    parrains = models.ManyToManyField('self', related_name='fillots', symmetrical = False, blank=True, null=True)
    reponses = models.ManyToManyField(Reponse, blank=True)    
    
    class Meta:
        ordering = ['-promo','last_name']
    
    def __unicode__(self):
        return self.user.username
    
    @staticmethod        
    def premiere_annee():
        from django.db.models import Max 
        return UserProfile.objects.all().aggregate(Max('promo'))['promo__max']
        
    def en_premiere_annee(self):
        premiere_annee = UserProfile.premiere_annee()
        return (premiere_annee == self.promo)
    
    @property
    def nb_victoires_sondages(self):
        from sondages.models import Sondage, Vote
        from django.db.models import F, Count
        return Vote.objects.filter(eleve = self).exclude(sondage__resultat = 0).filter(choix = F('sondage__resultat')).count()
	
    @property
    def nb_defaites_sondages(self):
        from sondages.models import Sondage, Vote
        from django.db.models import F, Count
        return Vote.objects.filter(eleve = self).exclude(sondage__resultat = 0).exclude(choix = F('sondage__resultat')).count()
    
    @property
    def nb_participations_sondages(self):
        from sondages.models import Sondage, Vote
        return Vote.objects.filter(eleve = self).exclude(sondage__resultat = 0).count()
	
    @property
    def pourcentage_sondages(self):
        return self.nb_victoires_sondages / float(self.nb_participations_sondages)

    def get_absolute_url(self):
        return '/people/'+self.user.username    
        
    def separation_successeurs(self):
        successeurs = []
        if self.parrains.all:
            successeurs.extend(self.parrains.all())
        if self.fillots.all:
            successeurs.extend(self.fillots.all())
        if self.co.all:
            successeurs.extend(self.co.all())
        return successeurs

    @staticmethod    
    def find_shortest_path(start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        shortest = None
        for node in start.separation_successeurs():
            if node not in path:
                newpath = UserProfile.find_shortest_path(node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest
  
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

