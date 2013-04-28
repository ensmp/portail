from django.db import models
from django import forms
import os
import subprocess
from django.core.files import File

class Abatage(models.Model):
    fichier = models.FileField(upload_to='abatage')
    date = models.DateField()
    thumbnail = models.ImageField(max_length=300,upload_to='abatage/thumbnail/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super(Abatage, self).save(*args, **kwargs)
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
        ordering = ['-date']
    
    def __unicode__(self):
        return str(self.date.year)