from bde.models import Liste, Vote, Palum, ParrainageVoeux
from django.contrib import admin
from models import *

class PalumAdmin(admin.ModelAdmin):
    list_display = ('annee','date')
    list_filter = ('annee','date')

admin.site.register(Liste)
admin.site.register(Vote)
admin.site.register(Palum, PalumAdmin)
admin.site.register(ParrainageVoeux)
