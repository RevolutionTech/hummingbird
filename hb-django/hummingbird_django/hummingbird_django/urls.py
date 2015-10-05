from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hummingbird.views.index', name='index'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^hummingbird/',include('hummingbird.urls')),
    url(r'^hummingbird/', include('hummingbird.urls')),
)