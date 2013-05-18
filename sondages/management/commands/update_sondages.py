# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from sondages.models import Sondage
from trombi.models import UserProfile

class Command(BaseCommand):
    args = ''
    help = "met a jour les resultats des sondages"

    def handle(self, *args, **options):
        for sondage in Sondage.objects.filter(deja_paru = True).order_by('date_parution'):
            sondage.save()	
            print sondage.date_parution

        for eleve in UserProfile.objects.all():
            eleve.update_sondages()
            print eleve.last_name

        Sondage.objects.update_all_weights()
