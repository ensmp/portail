from django.template import Library, Node
from evenement.models import Evenement
from django import template
from django.db.models import Q
import datetime

     
register = Library()

class EventNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		start = datetime.date.today()
		max_days = 7
		days = [ start + datetime.timedelta(days=i) for i in xrange(0, max_days) ]

		events = []
		for d in days:
			for p in Evenement.objects.filter(date_debut__year=d.year, date_debut__month=d.month, date_debut__day=d.day).exclude(Q(is_personnel=True) & ~Q(createur__user__username=self.login.resolve(context))).order_by('date_debut'):
				events.append(p)

		context['events_list'] = events
		#context['events_list'] = Evenement.objects.filter(date_fin__gte = datetime.now()).order_by('date_debut')
		return ''
    
def obtenir_events(parser, token):
	return EventNode(token.contents.split()[1])
obtenir_events = register.tag(obtenir_events)