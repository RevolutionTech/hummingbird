from django.conf.urls import patterns, url

from songs.views import SongView

sv = SongView()

urlpatterns = patterns('',
	url(r'^assign_song/$', sv.assign_song, name='assign_song'),
	url(r'^add_uploaded_song/$', sv.add_uploaded_song, name='add_uploaded_song'),
)