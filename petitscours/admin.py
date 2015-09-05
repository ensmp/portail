from petitscours.models import PetitCours 
from django.contrib import admin


class PetitCoursAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'visible', 'niveau', 'matiere', 'attribue_a')
    list_filter = ['date_added', 'visible']
    search_fields = ['title']
    list_per_page = 100


admin.site.register(PetitCours,PetitCoursAdmin)
