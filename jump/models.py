from django.db import models
from trombi.models import UserProfile

# Create your models here.
class Etude(models.Model):
	titre = models.CharField(max_length=256)
	promo = models.IntegerField()
	description = models.TextField()
	contact = models.ForeignKey(UserProfile)
	date = models.DateTimeField(auto_now_add=True)
	requests = models.ManyToManyField(UserProfile,related_name='+', blank=True, null=True)
	encours = models.BooleanField()
	
	def __unicode__(self):
		return self.titre