from django.template import Library
from trombi.models import UserProfile
from objettrouve.models import ObjetTrouve
import datetime
     
register = Library()

@register.assignment_tag()
def obtenir_liste_objets(rang):
    objets = []
    liste = ObjetTrouve.objects.all()
    l = len(liste)
    indice = 0
    while indice < min(rang,l) :
    	objets = objets + [liste[indice]]
    	indice = indice +1

    return objets