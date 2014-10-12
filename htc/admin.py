from htc.models import Revue
from django.contrib import admin

class RevueAdmin(admin.ModelAdmin):
    list_display = ('titre','date')
    search_fields = ('titre','date')
    fields = ('fichier', 'titre', 'date', 'image_tag', 'thumbnail')
    readonly_fields = ('image_tag',)

admin.site.register(Revue, RevueAdmin)