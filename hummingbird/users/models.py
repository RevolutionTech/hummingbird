import datetime

from django.db import models
from django.contrib.auth.models import User

import config

class UserProfileManager(models.Manager):
	def get_if_has_not_played_today(self, mac_address):
		users_with_mac = self.filter(mac_address=mac_address)
		if users_with_mac:
			user_with_mac = users_with_mac[0]
			if user_with_mac.has_not_played_today():
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

	def has_not_played_today(self):
		# not played today if:
		# 	1) it's now after reset point and last played earlier today before reset point or earlier
		# 	2) it's now before reset point and last played earlier yesterday before reset point or earlier
		now = datetime.datetime.now()
		today = now.date()
		yesterday = today - datetime.timedelta(days=1)
		return (
			now.time() >= config.time_reset_time and self.most_recent_activity < datetime.datetime.combine(today, config.time_reset_time)
		) or (
			now.time() < config.time_reset_time and self.most_recent_activity < datetime.datetime.combine(yesterday, config.time_reset_time)
		)
