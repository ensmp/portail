from django.template import Library, Node
from todo.models import Todo
from django import template
from django.db.models import Q
from trombi.models import UserProfile
     
register = Library()

class TodoNode(Node):
	def __init__(self, login):
		Node.__init__(self)
		self.login = template.Variable(login)
			
	def render(self, context):
		context['todo_list'] = Todo.objects.filter(eleve__user__username=self.login.resolve(context))
		return ''
    
def obtenir_todos(parser, token):
	return TodoNode(token.contents.split()[1])
obtenir_todos = register.tag(obtenir_todos)