from psl.models import newsletter
from django.contrib import admin

class newsletterAdmin(admin.ModelAdmin):
    list_display = ('titre','date')
    search_fields = ('titre','date')
    fields = ('fichier', 'titre', 'date', 'image_tag', 'thumbnail')
    readonly_fields = ('image_tag',)

admin.site.register(newsletter, newsletterAdmin)
