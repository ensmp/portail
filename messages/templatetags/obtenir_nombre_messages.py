from django.template import Library, Node
from messages.models import Message
     
register = Library()
     
class LatestLinksNode(Node):
    def render(self, context):
       # context['recent_links'] = Message.objects.exclude(lu__user__username=request.user.username).exclude(important__user__username=request.user.username).count()
        return ''
    
def get_latest_links(parser, token):
    return LatestLinksNode()
#get_latest_links = register.tag(get_latest_links)

@register.simple_tag
def compter_messages(request):
    return Message.objects.exclude(lu__user__username=request.user.username).exclude(important__user__username=request.user.username).count()