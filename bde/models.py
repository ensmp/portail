# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from datetime import date, datetime, timedelta
from django.core.files import File
import subprocess
import os



class Liste(models.Model):    
    nom = models.CharField(max_length=32)
    couleur = models.CharField(max_length=7)
    debut_vote = models.DateTimeField(default=datetime.now)
    fin_vote = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.nom        
        
class Vote(models.Model):
    liste = models.ForeignKey(Liste)
    eleve = models.ForeignKey(UserProfile, related_name="votes_liste")
    
    def __unicode__(self):
        return self.eleve.user.username

class Palum(models.Model):
    """
        Le Palum, recueil annuel d'annales des examens aux Mines

        Le fonctionnement est le même que celui du module Vendôme
    """
    fichier = models.FileField(upload_to='palum', help_text="Au format pdf, ne doit pas dépasser 10mo environ")
    date = models.IntegerField(default=2012, help_text= "2012 pour l'année scolaire 2012/2013")
    annee = models.IntegerField(default=1, help_text= "1 pour 1A, 2 pour 2A, 3 pour 3A")
    thumbnail = models.ImageField(max_length=300, upload_to='palum/thumbnail/', blank=True, null=True, verbose_name="Miniature", help_text="Image générée automatiquement à l'envoi d'un Palum")

    class Meta:
        ordering = ['annee','-date']        
    
    def __unicode__(self):
        return str(self.annee) + ' - ' + str(self.date)
    
    def save(self, *args, **kwargs):
        """ Sauvegarder un palum, fonctionne comme pour les Vendômes"""
        super(Palum, self).save(*args, **kwargs)
        if not self.thumbnail:
            # Génération du fichier image par ligne de commande
            path_destination = os.path.dirname(self.fichier.path) + '/thumbnail/' # Chemin du dossier
            path_destination += os.path.basename(self.fichier.path).partition('.')[0] + '_thumb' + '.png' # Nom du fichier
            command = 'convert -thumbnail x300 ' + self.fichier.path + '[0] ' + path_destination
            if subprocess.call(command,shell=True) == 0:
                # On récupère le fichier généré pour mettre à jour le champ thumbnail
                f = File(open(path_destination,'r'))
                self.thumbnail.save(path_destination, f, True)
                print 'Thumbnail created!'

    def image_tag(self):
        """Tag html de l'image du thumbnail, utilisé dans l'administration des Palums."""
        return u'<img src="%s" />' % self.thumbnail.url
    image_tag.allow_tags = True