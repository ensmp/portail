from django.template import Library, Node
from entreprise.models import Entreprise
     
register = Library()
     
class EntrepriseNode(Node):
    def render(self, context):
        context['liste_des_entreprises'] = Entreprise.objects.order_by('ordre');
        return ''
    
def obtenir_entreprises(parser, token):
    return EntrepriseNode()
obtenir_entreprises = register.tag(obtenir_entreprises)