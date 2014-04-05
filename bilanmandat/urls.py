from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('bilanmandat.views',
    url(r'^voter/?$','voter'),
    url(r'^results/?$','results'),
    url(r'^proche/?$','proche'),
)