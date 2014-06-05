import datetime

from django.contrib import admin

import config
from utils import log, print_MAC_address
from users.models import *
from songs.models import Song
from network.admin import NetworkManager
from songs.admin import SongManager

class UserManager:
	def __init__(self):
		self.song_manager = SongManager()
		self.network_manager = NetworkManager(user_manager=self)

	def init_hummingbird(self):
		if config.all_users_no_activity_today:
			for user in UserProfile.objects.all():
				user.most_recent_activity = datetime.datetime.now() - datetime.timedelta(days=2)
				user.save()
		self.song_manager.init_mixer()
		self.network_manager.init_network()

	def create_user(self, email, mac_address, first_name, last_name='', username=None, password=None, delay=config.time_default_delay_to_play_song, song_title=None, song_artist="n/a", song_album="n/a", song_random=False, walkin_length=config.time_default_max_song_length):
		# get dynamic defaults
		if not username:
			username = first_name
		if not password:
			password = mac_address

		# create user and userprofile
		user = User.objects.create_user(username=username, email=email, password=password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		up = UserProfile.objects.create(user=user, mac_address=mac_address, delay=delay)
		
		# assign song (randomly if not given)
		if not song_title:
			self.song_manager.assign_random_song(user=up)
		else:
			self.song_manager.add_uploaded_song_and_assign(user=up, title=song_title, artist=song_artist, album=song_album, random=song_random, walkin_length=walkin_length)
		
		return up

	def MAC_detected(self, address):
		print_MAC_address(address=address)
		try:
			userprofile = UserProfile.objects.get(mac_address=address)
			if userprofile.has_not_played_today():
				log(message="Detected activity from {name}.".format(name=userprofile.user.first_name))
				userprofile.most_recent_activity = datetime.datetime.now()
				userprofile.save()
				self.song_manager.queue_song(user=userprofile.user)
		except UserProfile.DoesNotExist:
			pass
