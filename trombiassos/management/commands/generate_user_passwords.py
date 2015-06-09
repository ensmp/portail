# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = ''
    help = "Genere des mots de passe aleatoires pour tous les utilisateurs"

    def handle(self, *args, **options):
        for user in User.objects.all():
            password = User.objects.make_random_password()
            self.stdout.write(user.username + ' - ' + password + '\n')
            user.set_password(password)
            user.save()
        self.stdout.write('mots de passe generes')