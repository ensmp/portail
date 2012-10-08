from django.db import models
from django import forms
import os
import subprocess
from django.core.files import File

class Vendome(models.Model):
    titre = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='vendome')
    date = models.DateField()
    thumbnail = models.ImageField(max_length=300,upload_to='vendome/thumbnail/', blank=True, null=True)
    is_hidden_1A = models.BooleanField()
	
    def save(self, *args, **kwargs):
        super(Vendome, self).save(*args, **kwargs)
        if not self.thumbnail:   
            path_destination = os.path.dirname(self.fichier.path) + '/thumbnail/' 
            path_destination += os.path.basename(self.fichier.path).partition('.')[0] + '_thumb' + '.png'
            comand = 'convert -thumbnail x300 ' + self.fichier.path + '[0] ' + path_destination
            if subprocess.call(comand,shell=True) == 0:
                f = File(open(path_destination,'r'))
                self.thumbnail.save(path_destination, f, True)
                print 'Thumbnail created!'

    class Meta:
        ordering = ['-date']
    
    def __unicode__(self):
        return self.titre    


class UploadFileForm(forms.Form):
    titre = forms.CharField(max_length=50)
    fichier  = forms.FileField()
    date  = forms.DateField()
    is_hidden_1A = forms.BooleanField()
