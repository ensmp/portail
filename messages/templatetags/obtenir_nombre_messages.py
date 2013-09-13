from django.template import Library, Node
from messages.models import Message
from django import template
from django.db.models import Q
from trombi.models import UserProfile
     
register = Library()

class NombreMessagesNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		eleve = UserProfile.objects.get(user__username = self.login.resolve(context))
		context['nombre_de_messages'] = Message.accessibles_par(eleve).exclude(lu = eleve).count()
		return ''
    
def compter_messages(parser, token):
	return NombreMessagesNode(token.contents.split()[1])
compter_messages = register.tag(compter_messages)
	

@register.filter("truncate_chars")
def truncate_chars(value, max_length):
	if len(value) <= max_length:
		return value
	truncd_val = value[:max_length]
	if value[max_length] != " ":
		rightmost_space = truncd_val.rfind(" ")
		if rightmost_space != -1:
			truncd_val = truncd_val[:rightmost_space]

	return truncd_val + "..."