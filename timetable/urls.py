from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('timetable.views',
	(r'^(?P<codes>[^\.]+).ics$', 'getics'),
	(r'','index'),
)