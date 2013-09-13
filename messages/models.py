# -*- coding: utf-8 -*-
from django.db import models
from trombi.models import UserProfile
from association.models import Association
from datetime import date, datetime, timedelta
from django import forms
from django.forms import ModelForm
from tinymce.widgets import TinyMCE
from notification.models import Notification
from django.db.models import Q
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic




from HTMLParser import HTMLParser
import htmlentitydefs

class HTMLTextExtractor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = [ ]

    def handle_data(self, d):
        self.result.append(d)

    def handle_charref(self, number):
        codepoint = int(number[1:], 16) if number[0] in (u'x', u'X') else int(number)
        self.result.append(unichr(codepoint))

    def handle_entityref(self, name):
        codepoint = htmlentitydefs.name2codepoint[name]
        self.result.append(unichr(codepoint))

    def get_text(self):
        return u''.join(self.result)


# Les messages d'association
class Message(models.Model):
    association = models.ForeignKey(Association)
    objet = models.CharField(max_length=300)
    contenu = models.TextField()
    date = models.DateTimeField(default=datetime.now(), blank=True)
    expediteur = models.ForeignKey(UserProfile) #L'élève qui a rédigé le message
 
    lu = models.ManyToManyField(UserProfile,related_name='message_lu', blank=True) #Les élèves qui ont lu le message
    important = models.ManyToManyField(UserProfile,related_name='message_important', blank=True) #Les élèves qui ont classé le message comme important

    commentaires = generic.GenericRelation(Comment, object_id_field="object_pk")
    notification = generic.GenericRelation(Notification)

    class Meta:
        ordering = ['-date']
    
    def get_absolute_url(self):
        return self.association.get_absolute_url() + 'messages/'
  
    def __unicode__(self):
        return self.objet

    @property
    def est_recent(self):
        return (self.date.date() == date.today())
    
    def envoyer_message_notification(self):
        message = self.association.nom + ' a publie un nouveau message'
        notification = Notification(content_object=self, description=message)
        notification.save()
        notification.envoyer_multiple(self.association.suivi_par.all())
        
    
    def envoyer_commentaire_notification(self, comment_pk, username):
        eleve = UserProfile.objects.get(user__username = username)
        message = eleve.first_name + ' ' + eleve.last_name + ' a commente un message de ' + self.association.nom
        commentaire = Comment.objects.get(pk = comment_pk)
        notification = Notification(content_object=commentaire, description=message)
        notification.save()
        notification.envoyer_multiple(self.association.suivi_par.all())
                
    def save(self, *args, **kwargs):
        creation = self.pk is None #Creation de l'objet         
        super(Message, self).save(*args, **kwargs)
        if creation:            
            self.envoyer_message_notification()
            
    def html_to_text(self):
        s = HTMLTextExtractor()
        s.feed(self.contenu)
        return s.get_text()

    @staticmethod
    def accessibles_par(eleve):
        return Message.objects.filter(date__gte = eleve.date_entree_aux_mines())

    
class MessageForm(ModelForm):
    contenu = forms.CharField(widget=TinyMCE(attrs={'cols': 120, 'rows': 30}))

    class Meta:
        model = Message
        fields = ('objet', 'contenu')
        
        
