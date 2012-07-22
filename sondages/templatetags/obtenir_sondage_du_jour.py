#-*- coding: utf-8 -*-
from django.template import Library, Node
from sondages.models import Sondage, Vote
from django import template
from django.db.models import Q
from trombi.models import UserProfile
from django.shortcuts import render_to_response, get_object_or_404
import datetime

     
register = Library()

class SondageNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		sondage = None
		#Nettoyage
		if Sondage.objects.filter(deja_paru = False, date_parution__lte = datetime.date.today() - datetime.timedelta(days=1)).exists(): #Il y a eu un sondage la veille
				sondage_hier = get_object_or_404(Sondage, deja_paru = False, date_parution__lte = datetime.date.today() - datetime.timedelta(days=1))
				sondage_hier.deja_paru = True
				sondage_hier.save()
		
		if Sondage.objects.filter(deja_paru = False, date_parution = datetime.date.today()).exists(): #Le sondage du jour a déjà été choisi
			sondage = get_object_or_404(Sondage, deja_paru = False, date_parution = datetime.date.today())
		else:			
			if Sondage.objects.filter(deja_paru = False, autorise = True).count() > 0 :
				sondage = Sondage.objects.filter(deja_paru = False, autorise = True).order_by('?')[0] #Le nouveau sondage du jour
				sondage.date_parution = datetime.date.today()
				sondage.save()
				
		if sondage:
			context['sondage'] = sondage
			if Vote.objects.filter(sondage = sondage, eleve__user__username=self.login.resolve(context)).exists(): #L'élève a déjà voté
				context['a_vote'] = True
				context['nombre_votes'] = Vote.objects.filter(sondage = sondage).count()
				context['nombre_votes_1'] = Vote.objects.filter(sondage = sondage, choix = 1).count()
				context['nombre_votes_2'] = Vote.objects.filter(sondage = sondage, choix = 2).count()				
		
		return ''
    
def obtenir_sondage(parser, token):
	return SondageNode(token.contents.split()[1])
obtenir_sondage = register.tag(obtenir_sondage)