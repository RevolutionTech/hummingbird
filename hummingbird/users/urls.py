from django.conf.urls import patterns, url

from users.views import UserView

uv = UserView()

urlpatterns = patterns('',
	url(r'^create_user/$', uv.create_user, name='create_user'),
	#url(r'^login_user/$', uv.login_user, name='login_user'),
)