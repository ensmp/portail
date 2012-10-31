# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from trombi.models import UserProfile
import json

class Command(BaseCommand):
    args = '<username...>'
    help = "trouve le plus court chemin entre deux utilisateurs"

    
    def handle(self, *args, **options):    
        if len(args) < 2:
            print 'entrez les usernames de depart et arrivee'
        else:
            start_username = args[0]
            end_username = args[1]
            
            start = UserProfile.objects.get(user__username = start_username)
            goal = UserProfile.objects.get(user__username = end_username)
            result = []
            if UserProfile.depthFirstSearch(start, goal, result):
                print 'resultat : ', [u.user.username for u in result]
            else:
                print 'pas de resultat'
            