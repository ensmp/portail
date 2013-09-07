# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from datetime import date, datetime, timedelta
from django import forms
import os
import subprocess
from django.core.files import File


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
    fichier = models.FileField(upload_to='palum') #fichier PDF, ne doit pas depasser 10mo environ
    date = models.IntegerField(default=2012,help_text= "2012 pour l'année scolaire 2012/2013") #Date de parution
    annee =  models.IntegerField(default=1,help_text= "1 pour 1A / 2 pour 2A /3 pour 3A") #1 pour 1A / 2 pour 2A ...
    thumbnail = models.ImageField(max_length=300,upload_to='palum/thumbnail/', blank=True, null=True) #image miniature, generee automatiquement a la creation par imagemagick
    
    def save(self, *args, **kwargs):
        super(Palum, self).save(*args, **kwargs)
        if not self.thumbnail:   
            # creation du thumbnail avec imagemagick
            path_destination = os.path.dirname(self.fichier.path) + '/thumbnail/' 
            path_destination += os.path.basename(self.fichier.path).partition('.')[0] + '_thumb' + '.png'
            command = 'convert -thumbnail x300 ' + self.fichier.path + '[0] ' + path_destination
            if subprocess.call(command,shell=True) == 0:
                f = File(open(path_destination,'r'))
                self.thumbnail.save(path_destination, f, True)
                print 'Thumbnail created!'

    class Meta:
        ordering = ['annee','-date']



class UploadFileForm(forms.Form):
    fichier  = forms.FileField()
    annee = forms.IntegerField()
    date  = forms.IntegerField()