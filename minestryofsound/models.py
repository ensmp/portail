from django.db import models
from django import forms

class Morceau(models.Model):
    artiste = models.CharField(max_length=50)
    titre = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='minestryofsound')
    date = models.DateField()
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "morceaux"
    
    def __unicode__(self):
        return self.titre    


class UploadFileForm(forms.Form):
    artiste = models.CharField(max_length=50)
    titre = forms.CharField(max_length=50)
    fichier  = forms.FileField()
    date  = forms.DateField()
