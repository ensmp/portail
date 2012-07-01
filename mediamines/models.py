from django.db import models
from datetime import date, datetime

# Create your models here.
class Album(models.Model):
    titre = models.CharField(max_length=300)    
    description =  models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=True)
    lieu = models.CharField(max_length=300)
    dossier = models.CharField(max_length=300)

    def __unicode__(self):
        return self.titre