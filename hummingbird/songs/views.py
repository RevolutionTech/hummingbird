from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from utils import create_kwargs
from songs.admin import SongManager

class SongView(View):
	def __init__(self):
		self.sm = SongManager()
	
	# TODO: Require user-login
	def assign_song(self, request):
		params = [	('title', unicode),
					('walkin_length', int)]
		kwargs = create_kwargs(request=request, params=params)
		if 'title' in kwargs:
			self.sm.assign_song(**kwargs)
		else:
			self.sm.assign_random_song(**kwargs)

	# TODO: Require user-login
	def add_uploaded_song(self, request):
		params = [	('title', unicode, False),
					('artist', unicode),
					('album', unicode),
					('random', bool),
					('assign', bool)]
		kwargs = create_kwargs(request=request, params=params)
		if 'assign' in kwargs:
			self.sm.add_uploaded_song_and_assign(**kwargs)
		else:
			self.sm.add_uploaded_song(**kwargs)
	