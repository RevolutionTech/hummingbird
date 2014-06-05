from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from utils import create_kwargs
from users.admin import UserManager

class UserView(View):
	def __init__(self):
		self.um = UserManager()

	def init_hummingbird(self, request):
		self.um.init_hummingbird()
		html = "<html><body>Hummingbird is now activated.</body></html>"
		return HttpResponse(html)

	def create_user(self, request):
		params = [	('email', unicode, False),
					('mac_address', unicode, False),
					('first_name', unicode, False),
					('last_name', unicode),
					('username', unicode),
					('password', unicode),
					('delay', int),
					('song_title', unicode),
					('song_artist', unicode),
					('song_album', unicode),
					('song_random', bool),
					('walkin_length', int)]
		kwargs = create_kwargs(request=request, params=params)
		self.um.create_user(**kwargs)
	