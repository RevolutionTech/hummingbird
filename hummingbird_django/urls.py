from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    url(r'^$', 'hummingbird.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hummingbird/', include('hummingbird.urls')),
)
