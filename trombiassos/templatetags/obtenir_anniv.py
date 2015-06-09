from django.template import Library
from trombi.models import UserProfile
import datetime
     
register = Library()

@register.assignment_tag()
def obtenir_liste_annivs(range):
    days = [datetime.date.today() + datetime.timedelta(days=i) for i in xrange(0, range)]
    people = []
    for d in days:
    	people.extend(UserProfile.objects.promos_actuelles().filter(birthday__month=d.month, birthday__day=d.day).all())
    return people