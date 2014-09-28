import datetime

from django.db import models
from django.contrib.auth.models import User

import config
from utils import has_not_played_today

class UserProfileManager(models.Manager):
	has_played = {}

	def get_if_has_not_played_today(self, mac_address):
		now = datetime.datetime.now()
		user_with_mac = None

		# Get the time we last saw this mac address (either from cache or db)
		if mac_address in self.has_played:
			last_seen, last_updated = self.has_played[mac_address]
		else:
			try:
				user_with_mac = self.get(mac_address=mac_address)
				last_seen = last_updated = user_with_mac.most_recent_activity
			except UserProfile.DoesNotExist:
				last_seen = last_updated = now

		# Determine if this mac has played today or not
		has_played_today = not has_not_played_today(dt=last_seen)

		# Update last seen and last updated
		last_seen = now
		if last_updated < now - datetime.timedelta(minutes=10):
			# Update in db
			last_updated = now
			try:
				if not user_with_mac:
					user_with_mac = self.get(mac_address=mac_address)
				user_with_mac.most_recent_activity = now
				user_with_mac.save()
			except UserProfile.DoesNotExist:
				pass

		# Update cache
		self.has_played[mac_address] = (last_seen, last_updated)

		# Return the user if not played today
		if not has_played_today:
			return user_with_mac

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	mac_address = models.CharField(max_length=17, unique=True, db_index=True)
	walkin_song = models.ForeignKey('songs.SongAssignment', null=True, blank=True)
	delay = models.IntegerField(default=config.time_default_delay_to_play_song, blank=True)
	most_recent_activity = models.DateTimeField(auto_now_add=True, blank=True)

	objects = UserProfileManager()

	def __unicode__(self):
		return "{user}: {song} ({song_length}s)".format(user=self.user, song=self.walkin_song.song, song_length=self.walkin_song.walkin_length)
