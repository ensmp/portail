from evenement.models import Evenement
from django.contrib import admin

class EvenementAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'association', 'date_debut')

admin.site.register(Evenement, EvenementAdmin)
