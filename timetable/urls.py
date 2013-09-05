from django.conf.urls.defaults import *

urlpatterns = patterns('timetable.views',
	(r'^mines\.ics$', 'getics'),
	(r'','index'),
)