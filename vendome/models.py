from django.db import models
from django import forms

class Vendome(models.Model):
    titre = models.CharField(max_length=50)
    fichier = models.FileField(upload_to='vendome')
    date = models.DateField()
	
    class Meta:
        ordering = ['-date']
	
    def __unicode__(self):
        return self.titre	


class UploadFileForm(forms.Form):
    titre = forms.CharField(max_length=50)
    fichier  = forms.FileField()
    date  = forms.DateField()
