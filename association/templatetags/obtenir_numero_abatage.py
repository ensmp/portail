# -*- coding: utf-8 -*-
from django.template import Library, Node
from association.models import Association
     
register = Library()
     
class AssociationsNumberNode(Node):
    def render(self, context):
        context['numeros'] = {"BDE": "15", "BDA": "18", "BDS": "31", "MediaMines": "19", "Vendome": "27", "MinesMarket": "20", "JuMP": "17", "Forum Trium": "17", "Biéro": "25", "MineShake": "26", "MINEStry of Sound": "29", "MDS": "22", "WEI": "16", "ASTi": "16", "Petite Revue": "27", "Club Rock": "28", "CAV": "25", "Rezal": "19", "Cahier Vert": "18", "Voyage Promo": "13", "CC": "19", "Royal Fucking Fanfare": "26", "Club Voile": "28", "Ski Club": "28", "Abatage": "27", "Minotaure": "20", "Handivalides": "20", "Routes de la Soie": "21", "Macadam": "22", "MineStream": "29", "GLAM": "19"};
        return ''
    
def obtenir_numero_association_abatage(parser, token):
    return AssociationsNumberNode()
obtenir_numero_association_abatage = register.tag(obtenir_numero_association_abatage)

