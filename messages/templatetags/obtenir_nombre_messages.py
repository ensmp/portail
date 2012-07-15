from django.template import Library, Node
from messages.models import Message
from django import template
from django.db.models import Q
from trombi.models import UserProfile
     
register = Library()

#@register.simple_tag
#def compter_messages(request):
#    return Message.objects.exclude(lu__user__username=request.user.username).exclude(important__user__username=request.user.username).count()

class NombreMessagesNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		context['nombre_de_messages'] = Message.objects.filter(Q(destinataire__isnull=True) | Q(destinataire__in=UserProfile.objects.get(user__username = self.login.resolve(context)).association_set.all()) | Q(association__in=UserProfile.objects.get(user__username = self.login.resolve(context)).association_set.all())).exclude(lu__user__username=self.login.resolve(context)).count()
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