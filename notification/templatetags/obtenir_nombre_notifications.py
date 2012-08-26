from django.template import Library, Node
from notification.models import Envoi
from django import template
from django.db.models import Q
from trombi.models import UserProfile
     
register = Library()

class NombreNotificationsNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		context['nombre_de_notifications'] = Envoi.objects.filter(user__username = self.login.resolve(context), lu=False).count()
		return ''
    
def compter_notifications(parser, token):
	return NombreNotificationsNode(token.contents.split()[1])
compter_notifications = register.tag(compter_notifications)
	