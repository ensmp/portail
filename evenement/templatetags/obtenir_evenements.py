from django.template import Library, Node
from evenement.models import Evenement
from django import template
from django.db.models import Q
     
register = Library()

class EventNode(Node):
	def __init__(self):
		Node.__init__(self)
			
	def render(self, context):
		context['events_list'] = Evenement.objects.all().order_by('date_debut')
		return ''
    
def obtenir_events(parser, token):
	return EventNode()
obtenir_events = register.tag(obtenir_events)