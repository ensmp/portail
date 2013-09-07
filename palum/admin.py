from palum.models import Palum
from django.contrib import admin
from models import *


class PalumAdmin(admin.ModelAdmin):
    list_display = ('annee','date')
    list_filter = ['annee','date']

admin.site.register(Palum, PalumAdmin)
