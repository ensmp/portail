# -*- coding: utf-8 -*-
from django.template import Library, Node
from association.models import Association
from collections import OrderedDict

register = Library()
     
class AbatagePageNode(Node):
    def render(self, context):
        pages = {"bde": "15", 
                 "bda": "18", 
                 "bds": "31", 
                 "mediamines": "19", 
                 "vendome": "27", 
                 "minesmarket": "20", 
                 "jump": "17", 
                 "trium": "17", 
                 "biero": "25", 
                 "mineshake": "26", 
                 "minestryofsound": "29", 
                 "mds": "22", 
                 "wei": "16", 
                 "asti": "16", 
                 "pr": "27", 
                 "rock": "28", 
                 "cav": "25", 
                 "rezal": "19", 
                 "cahiervert": "18", 
                 "vp": "13", 
                 "cc": "19", 
                 "fanfare": "26", 
                 "voile": "28", 
                 "skiclub": "28", 
                 "abatage": "27", 
                 "minotaure": "20", 
                 "handivalides": "20", 
                 "routes": "21", 
                 "macadam": "22", 
                 "mineStream": "29", 
                 "glam": "19"}
        abatage_pages_associations = {Association.objects.get(pseudo=pseudo):page for pseudo, page in pages.iteritems()}
        abatage_pages_associations = OrderedDict(sorted(abatage_pages_associations.items(), key=lambda x: x[0].ordre)) # Pour classer par page, choisir key=lambda x: x[1]
        context['abatage_pages_associations'] = abatage_pages_associations
        return ''
    
def obtenir_pages_associations_abatage(parser, token):
    return AbatagePageNode()
obtenir_pages_associations_abatage = register.tag(obtenir_pages_associations_abatage)

