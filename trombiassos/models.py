# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Count
from django.db.models.signals import post_save
import datetime

class Question(models.Model):
    """
        Une question pour le questionnaire du trombi
    """
    enonce = models.CharField(max_length=512, verbose_name="énoncé")
    def __unicode__(self):
        return self.enonce

class Reponse(models.Model):
    """
        La réponse d'un élève à une question
    """
    question = models.ForeignKey(Question)
    contenu = models.CharField(max_length=512, help_text="Le texte de la réponse à la question")
    
    class Meta:
        verbose_name="réponse"
            
    def __unicode__(self):
        return str(self.question.id) + ' -> ' + self.contenu

class UserProfileManager(models.Manager):    
    def promos_actuelles(self, nombre=4):
        """
            Les 1A, 2A, 3A et 4A actuels uniquement.
            On peut spécifier le nombre de promos souhaitées en argument.
        """
        promo_max = UserProfile.premiere_annee() - nombre
        return self.filter(promo__gte = promo_max).exclude(promo = promo_max, est_cesurien = False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, help_text="Le compte utilisateur associé au profil")
    objects = UserProfileManager()

    #Identité
    first_name = models.CharField(max_length=128, verbose_name="prénom")
    last_name = models.CharField(max_length=128, verbose_name="nom de famille")
    surnom = models.CharField(max_length=128, blank=True, default="")    
    birthday = models.DateField(null=True, verbose_name="date de naissance")
    est_une_fille = models.BooleanField()

    # Infos pratiques
    promo = models.IntegerField(null=True)
    option = models.CharField(max_length=128, blank=True)
    est_ast = models.BooleanField()
    est_cesurien = models.BooleanField()
    phone = models.CharField(max_length=15, blank=True, verbose_name="numéro de téléphone")
    a_la_meuh = models.BooleanField(default=True, verbose_name="à la meuh", help_text="Si l'élève loge à la Meuh")
    chambre = models.CharField(max_length=128, blank=True, verbose_name="numéro de chambre")
    adresse_ailleurs = models.CharField(max_length=512, blank=True, help_text="Adresse en dehors de la Meuh") 
    
    # Vie aux Mines
    sports = models.CharField(max_length=512, blank=True)
    co = models.ManyToManyField('self', symmetrical = True, blank=True, null=True)
    parrains = models.ManyToManyField('self', related_name='fillots', symmetrical = False, blank=True, null=True)
    reponses = models.ManyToManyField(Reponse, editable=False, blank=True, verbose_name="réponses", help_text="Ses réponses aux questionnaire du trombi")
    solde_octo = models.FloatField(default=0)
    solde_biero = models.FloatField(default=0, verbose_name="solde biéro")
    solde_minesmarket = models.FloatField(default=0, verbose_name="solde minesmarket")
    solde_freshbox = models.FloatField(default=0, verbose_name="solde freshbox")
    solde_mineshake = models.FloatField(default=0, verbose_name="solde mineshake")
    solde_bda = models.FloatField(default=0, verbose_name="solde bda")
    solde_paindemine = models.FloatField(default=0, verbose_name = "solde pain de mine")
    
    # Statistiques des sondages
    victoires_sondages = models.IntegerField(editable=False, help_text="Le nombre de sondages auxquels l'élève a voté selon la majorité")
    participations_sondages = models.IntegerField(editable=False, help_text="Le nombre de sondages auxquels l'élève a voté")
    score_victoires_sondages = models.FloatField(editable=False, help_text="Le rang au classement Wilson des consensuels dans les statistiques des sondages")
    score_defaites_sondages = models.FloatField(editable=False, help_text="Le rang au classement Wilson des libres penseurs dans les statistiques des sondages")

    # Statistiques jeux

    meilleur_score_2048 = models.IntegerField(default=0, blank=True, null=True, editable=False, help_text="Meilleur score à 2048")

    ################
    ### Méthodes ###
    ################

    class Meta:
        ordering = ['-promo','last_name']
        verbose_name="profil"
    
    def __unicode__(self):
        return '%s %s' % (self.first_name.title(), self.last_name.title())

    def get_absolute_url(self):
        return '/people/'+self.user.username
    
    def update_solde_minesmarket(self,prix):
        self.solde_minesmarket = self.solde_minesmarket - float(prix)
        self.save()    

    def update_solde_paindemine(self,prix):
        self.solde_paindemine = self.solde_paindemine - float(prix)
        self.save()
    
    def update_solde_freshbox(self,prix):
        self.solde_freshbox = self.solde_freshbox - float(prix)
        self.save()

    def update_solde_bda(self,prix):
        self.solde_bda = self.solde_bda - float(prix)
        self.save()

    def update_solde_mineshake(self,prix):
        self.solde_mineshake = self.solde_mineshake - float(prix)
        self.save()
    ### Années ###

    @staticmethod        
    def premiere_annee():
        """Renvoie le maximum des promos des élèves inscrits sur le portail"""
        from django.db.models import Max 
        return UserProfile.objects.all().aggregate(Max('promo'))['promo__max']
        
    def annee(self, premiere_annee=None):
        """L'année de l'élève: 1 pour 1A, 2 pour 2A, 3 pour 3A, etc."""
        if not premiere_annee:
            premiere_annee = UserProfile.premiere_annee()
        annee = premiere_annee - self.promo + 1
        if self.est_cesurien:
            annee -= 1
        return annee
    
    def en_premiere_annee(self):
        """Si l'élève fait sa première année aux mines. 1A, ou 2A AST."""
        return (self.annee() == 1) or ((self.annee() == 2) and self.est_ast)

    def date_entree_aux_mines(self):
        """Renvoie la date à laquelle l'élève est arrivé aux mines"""
        return datetime.date(2000 + self.promo, 9, 1) #Le premier septembre de l'année de sa promotion

    
    ### Statistiques des sondages ###

    @property
    def defaites_sondages(self):
        """Renvoie le nombre de sondages auxquels l'élève a voté selon la minorité"""
        return self.participations_sondages - self.victoires_sondages
    
    def update_sondages(self):
        """Met à jour les variables concernant les statistiques de sondages de l'élève"""
        from sondages.models import Sondage, Vote
        from math import sqrt

        votes = Vote.objects.filter(eleve = self).exclude(sondage__resultat = 0)
        self.victoires_sondages = votes.filter(choix = F('sondage__resultat')).count()
        self.participations_sondages = votes.count()
        
        n = self.participations_sondages        
        if n == 0:
            self.score_sondages = 0
        else: # Wilson lower bound
            z = 1.64485 # 1.0 = 85%, 1.6 = 95%
            phi = float(self.victoires_sondages)/n
            self.score_victoires_sondages = 100*(phi+z*z/(2*n)-z*sqrt((phi*(1-phi)+z*z/(4*n))/n))/(1+z*z/n)
            phi = float(n-self.victoires_sondages)/n
            self.score_defaites_sondages = 100*(phi+z*z/(2*n)-z*sqrt((phi*(1-phi)+z*z/(4*n))/n))/(1+z*z/n)
        self.save()
    
    @property
    def pourcentage_sondages(self):
        """Pourcentage de victoires sur les votes de l'élève aux sondages"""
        if self.participations_sondages == 0:
            return 0
        return float(100*self.victoires_sondages)/self.participations_sondages
        
    ### Degrés de séparation du trombi ###

    def separation_successeurs(self):
        """L'ensemble des voisins de l'élève sur le graphe des Mineurs"""
        successeurs = []
        if self.parrains.all:
            successeurs.extend(self.parrains.all())
        if self.fillots.all:
            successeurs.extend(self.fillots.all())
        if self.co.all:
            successeurs.extend(self.co.all())
        return successeurs
   
    def relation_avec(self, eleve):
        """
            Décrit la relation qui le lie avec un élève donné: parrain, fillot, co, etc. 
            Renvoie None si les deux élèves n'ont pas de liens directs
        """
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
    
    
    @staticmethod
    def BFS(start, end):
        """Algorithme de Breadth-First-Search, pour trouver le plus court chemin entre deux élèves"""
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

    @staticmethod
    def DFS(v):
        """Algorithme de Depth-First-Search, pour trouver la composante connexe d'un élève"""
        yield v
        visited = set ([v])
        S = v.separation_successeurs()
        while S:
            w = S.pop()
            if w not in visited:
                yield w
                visited.add (w)
                S.extend(w.separation_successeurs())

    ### Autres ###

    @property    
    def nb_petits_cours_attribues(self):
        """Renvoie le nombre de petits cours ayant déjà étés attribués à l'élève"""
        from petitscours.models import PetitCours
        return PetitCours.objects.filter(attribue_a = self.user).count()



def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil associé lorsqu'un utilisateur est créé"""
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
