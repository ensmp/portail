from django.db import models
from trombi.models import UserProfile

class Sondage(models.Model):
    question = models.CharField(max_length=512)
    reponse1 = models.CharField(max_length=50)
    reponse2 = models.CharField(max_length=50)
    deja_paru = models.BooleanField()    
    date_parution = models.DateField(null=True, blank=True)
    autorise = models.BooleanField()
    
    def date_str(self):
        jour = str(self.date_parution.day)
        mois = str(self.date_parution.month)
        if self.date_parution.day < 10:
            jour = '0' + jour
        if self.date_parution.month < 10:
            mois = '0' + mois
        return jour + '/' + mois + '/' + str(self.date_parution.year)
    
    def __unicode__(self):
        return self.question
        
class Vote(models.Model):
    sondage = models.ForeignKey(Sondage)
    eleve = models.ForeignKey(UserProfile)
    choix = models.IntegerField()
    
    def __unicode__(self):
        return self.eleve.user.username + ' -> ' + self.sondage.question