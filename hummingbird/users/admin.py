import datetime

from django.contrib import admin

import config
from utils import Log
from users.models import *
from songs.models import Song, SongAssignment
from network.admin import NetworkManager
from songs.admin import SongManager

class UserManager:
	def __init__(self):
		self.song_manager = SongManager()
		self.network_manager = NetworkManager(user_manager=self)

	def init_hummingbird(self, wait_to_play=config.wait_to_play, no_activity_today=config.all_users_no_activity_today):
		if no_activity_today:
			for user in UserProfile.objects.all():
				user.most_recent_activity = datetime.datetime.now() - datetime.timedelta(days=2)
				user.save()
		self.song_manager.init_mixer(wait_to_play)
		self.network_manager.init_network()

	def create_user(self, create_email, create_mac_address, create_first_name, create_last_name='', create_username=None, create_password=None, create_password_confirm=None, create_delay=config.time_default_delay_to_play_song, create_song_id=None):
		# Put mac address in lowercase
		create_mac_address = create_mac_address.lower()

		# Use first name as username if not provided
		if not create_username:
			create_username = create_first_name

		# Perform checks
		if User.objects.filter(email=create_email).count() > 0:
			raise UserWarning("The email {email} has already been registered by another user.".format(email=create_email))
		if UserProfile.objects.filter(mac_address=create_mac_address).count() > 0:
			raise UserWarning("The mac address {mac address} has already been registered by another user.".format(mac_address=create_mac_address))
		if User.objects.filter(username=create_username).count() > 0:
			raise UserWarning("The username {username} has already been registered by another user. You must register with a different username.".format(username=create_username))
		if (create_password or create_password_confirm) and (not create_password or not create_password_confirm):
			raise UserWarning("Both the password and password confirm fields must be filled in to set a password for your account.")
		if create_password and len(create_password) < config.user_password_min_length:
			raise UserWarning("Passwords must be at least {password_min_length} characters long.".format(password_min_length=config.user_password_min_length))
		if create_password and create_password != create_password_confirm:
			raise UserWarning("Password and password confirm fields do not match.")

		# Use mac address as password if not provided
		if not create_password:
			create_password = create_mac_address

		# create user and userprofile
		user = User.objects.create_user(username=create_username, email=create_email, password=create_password)
		user.first_name = create_first_name
		user.last_name = create_last_name
		user.save()
		up = UserProfile.objects.create(user=user, mac_address=create_mac_address, delay=create_delay)
		
		# assign song (randomly if not given)
		if not create_song_id:
			self.song_manager.assign_random_song(user=up)
		else:
			self.song_manager.assign_walkin_song(user=up, song=Song.objects.get(id=create_song_id))
		
		return up

	def update_user(self, user, email=None, username=None, password=None, password_confirm=None, first_name=None, last_name=None, mac_address=None, song_id=None, song_upload=None, delay=None):
		# Put mac address in lowercase
		if mac_address:
			mac_address = mac_address.lower()
		
		# Perform checks
		if email and email != user.user.email and User.objects.filter(email=email).count() > 0:
			raise UserWarning("The email {email} has already been registered by another user.".format(email=email))
		if username and username != user.user.username and User.objects.filter(username=username).count() > 0:
	 		raise UserWarning("The username {username} has already been registered by another user.".format(username=username))
		if (password or password_confirm) and (not password or not password_confirm):
			raise UserWarning("Both the password and password confirm fields must be filled in to update your password.")
		if password and len(password) < config.user_password_min_length:
			raise UserWarning("Password must be at least {password_min_length} characters long.".format(password_min_length=config.user_password_min_length))
		if password and password != password_confirm:
			raise UserWarning("Password and password confirm fields do not match.")
		if mac_address and mac_address != user.mac_address and UserProfile.objects.filter(mac_address=mac_address).count() > 0:
			raise UserWarning("The mac address {mac_address} has already been registered by another user.".format(mac_address=mac_address))

		# Update user
		if email:
			user.user.email = email
		if username:	
			user.user.username = username
		if password and password_confirm:
			user.user.set_password(password)
		if first_name:
			user.user.first_name = first_name
		if last_name:
			user.user.last_name = last_name
		if mac_address:
			user.mac_address = mac_address
		if song_upload:
			new_song = Song.objects.create(title=song_upload.name, audiofile=song_upload)
			user.walkin_song = SongAssignment.objects.create(user=user, song=new_song)
		elif song_id is not None:
			if song_id == 0:
				self.song_manager.assign_random_song(user=user)
			else:
				user.walkin_song, created = SongAssignment.objects.get_or_create(user=user, song=Song.objects.get(id=song_id))
		if delay is not None:
			user.delay = delay
		
		user.user.save()
		user.save()
		return user

	def MAC_detected(self, address):
		Log.log_MAC_address(address=address)
		try:
			userprofile = UserProfile.objects.get(mac_address=address)
			if userprofile.has_not_played_today():
				Log.log(message="Detected activity from {user}.".format(user=userprofile.user))
				userprofile.most_recent_activity = datetime.datetime.now()
				userprofile.save()
				self.song_manager.queue_song(user=userprofile.user)
		except UserProfile.DoesNotExist:
			pass
