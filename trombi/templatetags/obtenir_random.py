from django.template import Library, Node
from django import template
from django.db.models import Q
from trombi.models import UserProfile
from django.db.models import F




import random 

register = template.Library()

class NumberRandom(Node):
	def __init__(self):
		Node.__init__(self)
			
	def render(self, context):
		chiffre = str(random.randrange(0, 2))
		if chiffre=='0':
			context['bool']=True
		else :
			context['bool']=False
		chiffre2 = str(random.randrange(0, 2))
		if chiffre2=='0':
			context['bool2']=True
		else :
			context['bool2']=False
		return ''
    
def obtenir_nbr_random(parser, token):
	return NumberRandom()
obtenir_nbr_random = register.tag(obtenir_nbr_random)