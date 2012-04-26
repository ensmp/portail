from django.db import models
from django.contrib.auth.models import User

class PetitCours(models.Model):
	title = models.CharField(max_length=256)
	location = models.CharField(max_length=256)
	contact = models.CharField(max_length=256)
	date_added = models.DateTimeField(auto_now_add=True)
	date_given = models.DateTimeField(auto_now_add=True)
	visible = models.BooleanField()
	niveau = models.CharField(max_length=256)
	matiere = models.CharField(max_length=256) 
	description = models.CharField(max_length=512)
	requests = models.ManyToManyField(User,related_name='+', blank=True, null=True)

	visible.default = True

	def __unicode__(self):
		return self.title