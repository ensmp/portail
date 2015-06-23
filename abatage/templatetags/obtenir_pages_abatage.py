# -*- coding: utf-8 -*-
from django.template import Library, Node
from association.models import Association
from collections import OrderedDict
from django import template

register = template.Library()
     
class AbatagePageNode(Node):
    def render(self, context):
        pages = {"bde": "30", 
                 "bda": "34", 
                 "bds": "32", 
                 "mediamines": "40", 
                 "vendome": "44", 
                 "minesmarket": "20", 
                 "jump": "37", 
                 "trium": "36", 
                 "biero": "42", 
                 "mineshake": "43", 
                 "minotaure":"41",
                 "minestryofsound": "47", 
                 "mds": "22", 
                 "rezal":"40",
                 "cahiervert":"39",
                 "wei": "24", 
                 "asti": "38", 
                 "pr": "27", 
                 "rock": "47", 
                 "cav": "43", 
                 "rezal": "19", 
                 "cahiervert": "18", 
                 "vp": "28", 
                 "cc": "54", 
                 "fanfare": "46", 
                 "voile": "62", 
                 "skiclub": "63", 
                 "abatage": "27", 
                 "minotaure": "20", 
                 "handivalides": "20", 
                 "routes": "21", 
                 "macadam": "54", 
                 "mineStream": "29", 
                 "glam": "51"}
        abatage_pages_associations = {Association.objects.get(pseudo=pseudo):page for pseudo, page in pages.iteritems()}
        abatage_pages_associations = OrderedDict(sorted(abatage_pages_associations.items(), key=lambda x: x[0].ordre)) # Pour classer par page, choisir key=lambda x: x[1]
        context['abatage_pages_associations'] = abatage_pages_associations
        return ''
    
def obtenir_pages_associations_abatage(parser, token):
    return AbatagePageNode()
obtenir_pages_associations_abatage = register.tag(obtenir_pages_associations_abatage)

