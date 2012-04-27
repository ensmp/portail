from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta

# Create your models here.
class Message(models.Model):
 association = models.ForeignKey(Association)
 objet = models.CharField(max_length=300)
 contenu = models.TextField()
 date = models.DateTimeField(default=datetime.now(), blank=True)
 
 lu = models.ManyToManyField(UserProfile,related_name='message_lu', blank=True)
 important = models.ManyToManyField(UserProfile,related_name='message_important', blank=True)
  
 def __unicode__(self):
  return self.objet

 @property
 def est_recent(self):
    return (self.date.date() == date.today())


  
#class Commentaire(models.Model):
#  message = models.ForeignKey(Message)
#  auteur = models.ForeignKey(UserProfile)
#  contenu = models.TextField(_('body'))
#  date = models.DateTimeField(auto_now_add=True, blank=True)
  
#  def __unicode__(self):
#   return self.contenu