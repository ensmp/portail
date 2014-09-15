from django.contrib import admin
from trombi.models import UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(MachineProfile, MachineProfileAdmin)