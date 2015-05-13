from pr.models import Clip
from django.contrib import admin
from models import *
from pr.models import Candidat, Vote

admin.site.register(Clip)
admin.site.register(Vote)
admin.site.register(Candidat)