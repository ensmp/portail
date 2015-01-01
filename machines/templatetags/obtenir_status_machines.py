from django.template import Library, Node
from machines.models import MachineProfile
     
register = Library()
     
class MachinesNode(Node):
    def render(self, context):
        context['liste_des_machines'] = MachineProfile.objects.order_by('id');
        return ''
    
def obtenir_machines(parser, token):
    return MachinesNode()
obtenir_machines = register.tag(obtenir_machines)