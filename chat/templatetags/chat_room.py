from django.template import Library, Node
from django import template
from django.db.models import Q
from chat.models import Room
import datetime
from django.db.models import F

register = Library()

class RoomNode(Node):
	def __init__(self):
		Node.__init__(self)
			
	def render(self, context):
		
		context['room'] = Room.objects.latest('created')
		return ''
    
def obtenir_room(parser, token):
	return RoomNode()
obtenir_room = register.tag(obtenir_room)