from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponse

from users.views import UserView

uv = UserView()
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', uv.login, name='login'),
    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
    url(r'^init_hummingbird/', uv.init_hummingbird, name='init hummingbird'),
    url(r'^activity/', uv.activity, name='activity'),
    url(r'^profile/', uv.profile, name='profile'),
    url(r'^logout/', uv.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
