from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from songs.admin import SongManager

class SongView(View):
	def __init__(self):
		self.sm = SongManager()
	