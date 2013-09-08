# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import Group, User
from datetime import datetime
from notification.models import Notification, Envoi
from django.contrib.contenttypes import generic




#Une association, comme ensemble de membres
class Association(models.Model):
    nom = models.CharField(max_length=200)
    pseudo = models.SlugField()
    groupe_permissions = models.OneToOneField(Group, blank=True, null=True)
    membres = models.ManyToManyField(UserProfile, through='Adhesion', blank=True, null=True)
    suivi_par= models.ManyToManyField(User, related_name='associations_suivies', blank=True, null=True)    
    ordre = models.IntegerField(default=0)
 
    class Meta:
        ordering = ['ordre','nom']
 
    def __unicode__(self):
        return self.nom
 
    def save(self, *args, **kwargs):
        if not self.groupe_permissions: #On cree un groupe de permissions, si non-existant
            groupe = Group.objects.create(name=self.nom)
            self.groupe_permissions = groupe
        super(Association, self).save(*args, **kwargs) # Sauvegarde
        
    def get_absolute_url(self):
        return '/associations/' + self.pseudo + '/'

#Permet de préciser l'appartenance d'un membre à une assoce, et en particulier son rôle.
class Adhesion(models.Model):
    eleve = models.ForeignKey(UserProfile)
    association = models.ForeignKey(Association)
    role = models.CharField(max_length=64, blank=True) #role dans l'association
    ordre = models.IntegerField(default = 0) #ordre d'apparition dans la page 'equipe' de l'assoce
    
    class Meta:
        ordering = ['-ordre']
    
    def __unicode__(self):
        return self.eleve.user.username + ' -> ' + self.association.nom

    def save(self, *args, **kwargs):
        self.association.groupe_permissions.user_set.add(self.eleve.user) #On ajoute l'eleve au groupe de permissions
        super(Adhesion, self).save(*args, **kwargs) # Sauvegarde
        
    def delete(self):
        self.association.groupe_permissions.user_set.remove(self.eleve.user) #On retire l'eleve du groupe de permissions
        super(Adhesion, self).delete()

    @staticmethod
    def existe(eleve, association):
        return Adhesion.objects.filter(association=association, eleve=eleve).exists()
    
# Video sur la page medias d'une assoce
class Video(models.Model):
    association = models.ForeignKey(Association, blank=True, null=True)
    titre = models.CharField(max_length=64)
    url  = models.URLField(max_length=200)
    date = models.DateField(default=datetime.now)
    
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
        creation = self.pk is None #Creation de l'objet
        if self.url[:31] == 'http://www.youtube.com/watch?v=': # On reconnait un lien direct vers une video youtube
            self.url = 'http://www.youtube.com/embed/' + self.url[31:].split('&')[0]
        elif self.url[:29] == 'http://www.youtube.com/embed/': # On reconnait un lien embed vers une video youtube
            pass
        elif self.url[:18] == 'https://vimeo.com/': # On reconnait un lien direct vers une video vimeo
            self.url = 'http://player.vimeo.com/video/' + self.url[18:]
        elif self.url[:30] == 'http://player.vimeo.com/video/':
            pass
        else:
            self.url = ''
        super(Video, self).save(*args, **kwargs) # Sauvegarde
        if creation:            
            self.envoyer_notification()
        
# Les affiches pour la page medias d'une assoce
class Affiche(models.Model):
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
        creation = self.pk is None #Creation de l'objet            
        super(Affiche, self).save(*args, **kwargs)
        if creation:            
            self.envoyer_notification()
        

#Les pages personalisées des associations. On ne précise que le titre de la page et son url. La page en elle même est à implémenter dans une application ad-hoc.
class Page(models.Model):
    association = models.ForeignKey(Association)
    titre = models.CharField(max_length=200)
    lien = models.CharField(max_length=200)
    is_externe = models.BooleanField(help_text="Lien vers un site externe au portail", verbose_name = "est externe") 
    
    def __unicode__(self):
        return self.association.nom + ' - ' + self.titre

        
#FORMULAIRES
class AdhesionAjoutForm(forms.Form):

    eleve = forms.ModelChoiceField(queryset=UserProfile.objects.all())
    role = forms.CharField(max_length=100, required=False)
    
    def __init__(self, association, *args, **kwargs):
        super(AdhesionAjoutForm, self).__init__(*args, **kwargs)
        self.fields['eleve'].queryset = UserProfile.objects.exclude(id__in = [m.id for m in association.membres.all()])
        
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
