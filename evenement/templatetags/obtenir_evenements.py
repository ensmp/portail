from django.template import Library
from evenement.models import Evenement
import datetime
     
register = Library()

@register.assignment_tag()
def get_next_events(range):
    debut = datetime.date.today()
    fin = debut + datetime.timedelta(days=range)
    return Evenement.objects.filter(date_debut__range=(debut, fin)).order_by('date_debut')