from django.template import Library, Node
from association.models import Association
     
register = Library()
     
class AssociationsNode(Node):
    def render(self, context):
        context['liste_des_associations'] = Association.objects.order_by('ordre').exclude(is_hidden_1A = True);
        return ''
    
def obtenir_associations(parser, token):
    return AssociationsNode()
obtenir_associations = register.tag(obtenir_associations)