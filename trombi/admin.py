from trombi.models import UserProfile, Question, Reponse
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'promo')
    list_filter = ('promo',)
    search_fields = ('first_name', 'last_name', 'user__username')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Question)
admin.site.register(Reponse)
