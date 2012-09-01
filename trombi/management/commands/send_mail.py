# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    args = ''
    help = "Genere des mots de passe aleatoires pour tous les utilisateurs"

    def handle(self, *args, **options):
        send_mail('Subject here', 'Here is the message.', 'from@example.com', ['11leuren@mines-paristech.fr'], fail_silently=False)
        self.stdout.write('mail envoye')