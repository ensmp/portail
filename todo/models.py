from django.db import models
from trombi.models import UserProfile
from datetime import datetime


# Create your models here.
class Todo(models.Model):
	eleve = models.ForeignKey(UserProfile)
	contenu = models.TextField()
	date = models.DateTimeField(default=datetime.now(), blank=True)
	fait = models.BooleanField()