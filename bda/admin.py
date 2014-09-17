from bda.models import Revue, Maitrise, Instrument
from django.contrib import admin

class RevueAdmin(admin.ModelAdmin):
    list_display = ('titre','date')
    search_fields = ('titre','date')
    fields = ('fichier', 'titre', 'date', 'image_tag', 'thumbnail')
    readonly_fields = ('image_tag',)

admin.site.register(Revue, RevueAdmin)
admin.site.register(Maitrise)
admin.site.register(Instrument)