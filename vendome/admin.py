from vendome.models import Vendome
from django.contrib import admin

class VendomeAdmin(admin.ModelAdmin):
    list_display = ('titre', 'is_hidden_1A')
    list_filter = ('is_hidden_1A',)
    list_editable = ('is_hidden_1A',)
    search_fields = ('titre',)

    fields = ('fichier', 'titre', 'date', 'is_hidden_1A', 'image_tag', 'thumbnail')
    readonly_fields = ('image_tag',)

admin.site.register(Vendome, VendomeAdmin)
