from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('entreprise.views',
    url(r'^$','presentation_entreprises'),
    url(r'^contact/$','contact_entreprises'),
    url(r'^planning/$','planning'),
    url(r'^liste/$', 'index'),
)