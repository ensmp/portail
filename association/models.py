# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes import generic
from datetime import datetime
from trombi.models import UserProfile
from notification.models import Notification, Envoi

class Association(models.Model):
    nom = models.CharField(max_length=200)
    pseudo = models.SlugField(help_text="Nom dans les urls")
    membres = models.ManyToManyField(UserProfile, through='Adhesion', blank=True, null=True)
    is_hidden_1A = models.BooleanField(default=False, verbose_name="Cachée aux 1A")
    ordre = models.IntegerField(default=0, help_text="Ordre d'apparition dans la liste des associations (ordre alphabétique pour les valeurs égales)")
    suivi_par = models.ManyToManyField(User, related_name='associations_suivies', blank=True, null=True, help_text= "Les élèves recevant les notifications de l'association")    
    groupe_permissions = models.OneToOneField(Group, blank=True, null=True, help_text="Groupe de permissions correspondant à l'association")
 
    class Meta:
        ordering = ['ordre','nom']
 
    def __unicode__(self):
        return self.nom

    def est_cachee_a(self, eleve):
        return self.is_hidden_1A and eleve.en_premiere_annee()

    def save(self, *args, **kwargs):
        if not self.groupe_permissions: # On crée un groupe de permissions, si non-existant
            groupe = Group.objects.create(name=self.nom)
            self.groupe_permissions = groupe
        super(Association, self).save(*args, **kwargs) # Sauvegarde
        
    def get_absolute_url(self):
        return '/associations/' + self.pseudo + '/'

class Adhesion(models.Model):
    """
        Permet de préciser l'appartenance d'un membre 
        à une assoce, et en particulier son rôle.
    """
    eleve = models.ForeignKey(UserProfile, verbose_name="élève")
    association = models.ForeignKey(Association)
    role = models.CharField(max_length=64, blank=True, help_text="Rôle dans l'association")
    ordre = models.IntegerField(default = 0, help_text="Ordre décroissant d'apparition de l'élève dans la page 'équipe' de l'assoce")
    
    class Meta:
        ordering = ['-ordre']
    
    def __unicode__(self):
        return self.eleve.user.username + ' -> ' + self.association.nom

    def save(self, *args, **kwargs):
        self.association.groupe_permissions.user_set.add(self.eleve.user) # On ajoute l'élève au groupe de permissions
        super(Adhesion, self).save(*args, **kwargs) # Sauvegarde
        
    def delete(self):
        self.association.groupe_permissions.user_set.remove(self.eleve.user) # On retire l'élève du groupe de permissions
        super(Adhesion, self).delete()

    @staticmethod
    def existe(eleve, association):
        """
            Renvoie vrai si l'élève est membre de l'association
        """
        return Adhesion.objects.filter(association=association, eleve=eleve).exists()

class Video(models.Model):
    """
        Une vidéo sur la page 'médias' d'une association
    """
    association = models.ForeignKey(Association, blank=True, null=True)
    titre = models.CharField(max_length=64, help_text="Titre de la vidéo")
    url = models.URLField(max_length=200, help_text="Lien vers une vidéo Youtube ou Vimeo")
    date = models.DateField(default=datetime.now, help_text="Date de publication")
    notification = generic.GenericRelation(Notification)

    class Meta:
        ordering = ['-date', '-id']
    
    def __unicode__(self):
        return self.association.nom + ' - ' + self.titre
		
    def get_absolute_url(self):
        return self.association.get_absolute_url() + 'medias/'
        
    def envoyer_notification(self):        
        notification = Notification(content_object=self, description=self.association.nom+' a publie une nouvelle video')
        notification.save()
        notification.envoyer_multiple(self.association.suivi_par.all())
        
    def save(self, *args, **kwargs):
        creation = self.pk is None # Création de l'objet
        if self.url[:31] == 'http://www.youtube.com/watch?v=': # Lien direct vers une video youtube
            self.url = 'http://www.youtube.com/embed/' + self.url[31:].split('&')[0]
        elif self.url[:29] == 'http://www.youtube.com/embed/': # Lien embed vers une video youtube
            pass
        elif self.url[:18] == 'https://vimeo.com/': # Lien direct vers une video vimeo
            self.url = 'http://player.vimeo.com/video/' + self.url[18:]
        elif self.url[:30] == 'http://player.vimeo.com/video/': # Lien embed vers une video vimeo
            pass
        else:
            self.url = ''
        super(Video, self).save(*args, **kwargs) # Sauvegarde
        if creation:            
            self.envoyer_notification()
        
class Affiche(models.Model):
    """
        Une affiche sur la page "médias" d'une association
    """
    association = models.ForeignKey(Association, blank=True, null=True)
    titre = models.CharField(verbose_name='Titre de l\'affiche', max_length=64)
    fichier = models.ImageField(upload_to = 'affiches')
    date = models.DateField(verbose_name='Date de publication', default=datetime.now, blank=True, null=True)
    notification = generic.GenericRelation(Notification)
    
    class Meta:
        ordering = ['-date', '-id']
    
    def __unicode__(self):
        return self.association.nom + ' - ' + self.titre
        
    def get_absolute_url(self):
        return self.association.get_absolute_url() + 'medias/'
        
    def envoyer_notification(self):        
        notification = Notification(content_object=self, description=self.association.nom+' a publie une nouvelle affiche')
        notification.save()
        notification.envoyer_multiple(self.association.suivi_par.all())
        
    def save(self, *args, **kwargs):
        creation = self.pk is None # Création de l'objet
        super(Affiche, self).save(*args, **kwargs)
        if creation:            
            self.envoyer_notification()

class Page(models.Model):
    """
        Les pages personnalisées des associations. 
        On ne précise ici que le titre de la page et son url. 
        La page en elle-même est à implémenter dans une application séparée.
    """
    association = models.ForeignKey(Association)
    titre = models.CharField(max_length=200)
    lien = models.SlugField(max_length=200, help_text="URL de la page. Ne donner que le nom de l'association si la page est interne.")
    is_externe = models.BooleanField(help_text="Vrai si la page est un site externe au portail", verbose_name = "est externe") 
    
    def __unicode__(self):
        return self.association.nom + ' - ' + self.titre

###################
### FORMULAIRES ###
###################

class AdhesionAjoutForm(forms.Form):

    eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    role = forms.CharField(max_length=100, required=False)
    
    def __init__(self, association, *args, **kwargs):
        super(AdhesionAjoutForm, self).__init__(*args, **kwargs)
        ### On retire les membres actuels de la liste
        self.fields['eleve'].queryset = UserProfile.objects.exclude(id__in = [m.id for m in association.membres.all()])
        
class AdhesionModificationForm(forms.Form):
    role = forms.CharField(max_length=100, required=False)

class AdhesionSuppressionForm(forms.Form):

    eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    
    def __init__(self, association, *args, **kwargs):
        super(AdhesionSuppressionForm, self).__init__(*args, **kwargs)
        self.fields['eleve'].queryset = association.membres.all()
    
    
class AfficheForm(ModelForm):

    class Meta:
        model = Affiche
        exclude = ('association',)
        
class VideoForm(ModelForm):

    class Meta:
        model = Video
        exclude = ('association',)
