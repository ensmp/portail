from vendome.models import Vendome
from django.contrib import admin
from models import *


class VendomeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'is_hidden_1A')
    list_filter = ['date', 'is_hidden_1A']

admin.site.register(Vendome, VendomeAdmin)
