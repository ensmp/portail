from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('timetable.views',
	(r'^mines\.ics$', 'getics'),
	(r'','index'),
)