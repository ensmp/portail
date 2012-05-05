from django.template import Library, Node
from django import template
from django.db.models import Q
from trombi.models import UserProfile
import datetime
from django.db.models import F

register = Library()

class AnnivNode(Node):
	def __init__(self):
		Node.__init__(self)
			
	def render(self, context):
	
		start = datetime.date.today()
		max_days = 7
		days = [ start + datetime.timedelta(days=i) for i in xrange(0, max_days) ]

		birthdays = []
		for d in days:
			for p in UserProfile.objects.filter(birthday__month=d.month, birthday__day=d.day):
				birthdays.append(p)

		context['anniv_list'] = birthdays
		#UserProfile.objects.all#filter(birthday__gte = datetime.date.today().replace(year=F('birthday__year'))).order_by('-user__username')
		return ''
    
def obtenir_liste_annivs(parser, token):
	return AnnivNode()
obtenir_liste_annivs = register.tag(obtenir_liste_annivs)