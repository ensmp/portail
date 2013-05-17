# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date, timedelta
import Queue

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
    surnom = models.CharField(max_length=128, blank=True, default="")    
    
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

    solde_octo = models.FloatField(default=0)
    solde_biero = models.FloatField(default = 0)
    
    victoires_sondages = models.IntegerField(blank = True, null=True)
    participations_sondages = models.IntegerField(blank = True, null=True)
    score_victoires_sondages = models.FloatField(blank = True, null=True)
    score_defaites_sondages = models.FloatField(blank = True, null=True)
    
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
    def defaites_sondages(self):
        return self.participations_sondages - self.victoires_sondages
    
    def update_sondages(self):        
        from django.db.models import F
        from math import sqrt        
        self.victoires_sondages = self.vote_set.filter(choix = F('sondage__resultat')).count()
        self.participations_sondages = self.vote_set.count()
        
        if self.participations_sondages == 0:
            self.score_sondages = 0
        else: #Wilson lower bound
            z = 1.64485 #1.0 = 85%, 1.6 = 95%
            phi = float(self.victoires_sondages) / self.participations_sondages
            self.score_victoires_sondages = 100 * (phi+z*z/(2*n)-z*sqrt((phi*(1-phi)+z*z/(4*n))/n))/(1+z*z/n)
            phi = float(self.defaites_sondages()) / self.participations_sondages
            self.score_defaites_sondages = 100 * (phi+z*z/(2*n)-z*sqrt((phi*(1-phi)+z*z/(4*n))/n))/(1+z*z/n)
        self.save()
    
    @property
    def pourcentage_sondages(self):
        if self.participations_sondages == 0:
            return 0
        return 100.0 * self.victoires_sondages / float(self.participations_sondages)

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
   
    def relation_avec(self, eleve):
        if self in eleve.co.all():
            return "co"
        if self in eleve.parrains.all():
            if self.est_une_fille:
                return "marraine"
            else:
                return "parrain"
        if self in eleve.fillots.all():
            if self.est_une_fille:
                return "fillotte"
            else:
                return "fillot"
        return None
    
    @property    
    def nb_petits_cours_attribues(self):
        from petitscours.models import PetitCours
        return PetitCours.objects.filter(attribue_a = self.user).count()
    
   #Algorithme de Breadth-First-Search, pour trouver le plus court chemin entre deux élèves
    @staticmethod    
    def BFS(start, end):
        visited = []
        queue = []
        queue.append([start])
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                return path
            if not node.id in visited:
                visited.append(node.id)
                for adjacent in node.separation_successeurs():                    
                    new_path = list(path)
                    new_path.append(adjacent)
                    queue.append(new_path)
        return None

    #Algorithme de Depth-First-Search, pour trouver la composante connexe d'un élève
    @staticmethod
    def DFS(v):
        yield v
        visited = set ([v])
        S = v.separation_successeurs()
        while S:
            w = S.pop()
            if w not in visited:
                yield w
                visited.add (w)
                S.extend (w.separation_successeurs())
  
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

