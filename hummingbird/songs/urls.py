from django.conf.urls import patterns, url

from songs.views import SongView

sv = SongView()

urlpatterns = patterns('',
	#url(r'^create_user/$', uv.create_user, name='create_user'),
	#url(r'^login_user/$', uv.login_user, name='login_user'),
)