from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta

# Create your models here.
class Evenement(models.Model):
	association = models.ForeignKey(Association)
	titre = models.CharField(max_length=300)
	description =  models.TextField()
	date = models.DateTimeField(default=datetime.now(), blank=True)
	participants = models.ManyToManyField(UserProfile,related_name='evenement_participant', blank=True)
	
	def __unicode__(self):
		return self.titre