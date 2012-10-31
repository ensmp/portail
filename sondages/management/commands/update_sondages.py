# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from sondages.models import Sondage

class Command(BaseCommand):
    args = ''
    help = "met a jour les resultats des sondages"

    def handle(self, *args, **options):
        for sondage in Sondage.objects.filter(deja_paru = True).order_by('date_parution'):
            print sondage.question
            sondage.save()	