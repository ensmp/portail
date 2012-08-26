# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from notification.models import Notification
from datetime import date, datetime, timedelta

class Command(BaseCommand):
    args = ''
    help = "Supprime toutes les notifications vieilles d'une semaine"

    def handle(self, *args, **options):
        old_notifications = Notification.objects.filter(date__lt = date.today()-timedelta(days=7))
        self.stdout.write('%i notifications nettoyees' % old_notifications.count())
        old_notifications.delete()